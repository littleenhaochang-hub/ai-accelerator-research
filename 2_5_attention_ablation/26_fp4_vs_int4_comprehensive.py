import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
import math

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# Benchmark questions (subset for rapid testing, focus on diverse tasks)
QUESTIONS = [
    {"q": "If I have 5 apples and eat 2, how many are left?", "keys": ["3", "three"]},
    {"q": "What is 15 plus 27?", "keys": ["42"]},
    {"q": "Solve for x: 2x + 6 = 14", "keys": ["4", "four"]},
    {"q": "What is the capital of Japan?", "keys": ["Tokyo"]},
    {"q": "What is the chemical symbol for water?", "keys": ["H2O", "h2o"]},
    {"q": "Write a Python function 'add' to add two numbers.", "keys": ["def", "return", "add"]},
    {"q": "Translate 'Hello, world' into French.", "keys": ["Bonjour", "bonjour", "monde"]},
    {"q": "What is 10 multiplied by 5?", "keys": ["50", "fifty"]},
    {"q": "Name a large grey animal with a trunk.", "keys": ["elephant", "Elephant"]},
    {"q": "Why is the sky blue? Explain in 3 words.", "keys": ["scattering", "Rayleigh", "light", "atmosphere", "blue", "scattered", "sunlight"]}
]

def evaluate_answer(ans, keys):
    ans_lower = ans.lower()
    for k in keys:
        if k.lower() in ans_lower: return True
    return False

# --- Quantization Engines ---
def quantize_int4(tensor, block_size=None):
    """Standard INT4 Uniform Quantization (-8 to 7)"""
    qmin, qmax = -8, 7
    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.view(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return (q_tensor * scale).view(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

def quantize_fp4_e2m1(tensor, block_size=None):
    """
    Simulates OCP FP4 (E2M1) format quantization.
    1 sign bit, 2 exponent bits, 1 mantissa bit.
    Dynamic range is highly concentrated around zero.
    Representable positive values (unscaled) roughly: 0, 0.5, 1, 1.5, 2, 3, 4, 6
    We simulate this by mapping to the nearest FP4 representable value.
    """
    # Normalized FP4 (E2M1) positive levels (excluding subnormals for simplicity, mapping to closest relative scale)
    fp4_levels = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], device=tensor.device, dtype=tensor.dtype)
    
    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.view(-1, block_size)
        # For FP formats, scale is usually based on max absolute value matching the max representable value (6.0)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / 6.0
        scale = torch.clamp(scale, min=1e-5)
        
        normalized_tensor = torch.abs(tensor_blocked) / scale
        
        # Broadcast for nearest neighbor search
        diffs = torch.abs(normalized_tensor.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        
        # Apply sign and scale back
        q_tensor = torch.sign(tensor_blocked) * quantized_abs * scale
        return q_tensor.view(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / 6.0
        scale = torch.clamp(scale, min=1e-5)
        
        normalized_tensor = torch.abs(tensor) / scale
        diffs = torch.abs(normalized_tensor.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        
        q_tensor = torch.sign(tensor) * quantized_abs * scale
        return q_tensor

def quantize_int8(tensor):
    qmin, qmax = -128, 127
    max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
    scale = max_val / qmax
    scale = torch.clamp(scale, min=1e-5)
    q_tensor = torch.round(tensor / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    return q_tensor * scale

# --- Configurable Attention ---
# Globals set per iteration
ATTN_KV_BITS = 8 
ATTN_KV_FORMAT = "int" # INT or FP

ORIGINAL_FORWARD = Qwen2Attention.forward

def configurable_attention_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
    # A8 Input to Attention (Fixed for this study)
    hidden_states = quantize_int8(hidden_states)
    
    bsz, q_len, _ = hidden_states.size()
    query_states = self.q_proj(hidden_states)
    key_states = self.k_proj(hidden_states)
    value_states = self.v_proj(hidden_states)

    query_states = query_states.view(bsz, q_len, self.config.num_attention_heads, self.head_dim).transpose(1, 2)
    key_states = key_states.view(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)
    value_states = value_states.view(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)

    from transformers.models.qwen2.modeling_qwen2 import apply_rotary_pos_emb
    cos, sin = position_embeddings
    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, unsqueeze_dim=1)

    # KV Cache Quantization
    if ATTN_KV_BITS == 8:
        key_states = quantize_int8(key_states)
        value_states = quantize_int8(value_states)
    elif ATTN_KV_BITS == 4:
        if ATTN_KV_FORMAT == "fp":
            key_states = quantize_fp4_e2m1(key_states)
            value_states = quantize_fp4_e2m1(value_states)
        else:
            key_states = quantize_int4(key_states)
            value_states = quantize_int4(value_states)

    past_kv = past_key_value if past_key_value is not None else past_key_values
    if past_kv is not None:
        cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
        key_states, value_states = past_kv.update(key_states, value_states, self.layer_idx, cache_kwargs)

    import transformers.models.qwen2.modeling_qwen2 as qwen2_mod
    key_states = qwen2_mod.repeat_kv(key_states, self.config.num_attention_heads // self.config.num_key_value_heads)
    value_states = qwen2_mod.repeat_kv(value_states, self.config.num_attention_heads // self.config.num_key_value_heads)

    attn_weights = torch.matmul(query_states, key_states.transpose(2, 3)) / math.sqrt(self.head_dim)
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, : key_states.shape[-2]]
        attn_weights = attn_weights + causal_mask

    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=self.config.attention_dropout, training=self.training)

    attn_output = torch.matmul(attn_weights, value_states)
    attn_output = attn_output.transpose(1, 2).contiguous()
    attn_output = attn_output.reshape(bsz, q_len, self.config.hidden_size)
    
    attn_output = quantize_int8(attn_output)
    attn_output = self.o_proj(attn_output)

    if not output_attentions: attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

# --- FFN Configurable Linear (INT4 vs FP4) ---
FFN_ACT_FORMAT = "int" # INT or FP

class FFN_Block32_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features, self.out_features = original_linear.in_features, original_linear.out_features
        self.weight, self.bias = original_linear.weight, original_linear.bias
    def forward(self, x):
        if FFN_ACT_FORMAT == "fp":
            w = quantize_fp4_e2m1(self.weight, block_size=32)
            x_q = quantize_fp4_e2m1(x, block_size=32)
        else:
            w = quantize_int4(self.weight, block_size=32)
            x_q = quantize_int4(x, block_size=32)
        return F.linear(x_q, w, self.bias)

def apply_patch(model):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "lm_head" not in name:
            setattr(model, name, FFN_Block32_Linear(module))
        else: apply_patch(module)

def run():
    global ATTN_KV_BITS, ATTN_KV_FORMAT, FFN_ACT_FORMAT
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # 4 Core Configurations to trace the breakdown of INT4 vs FP4
    configs = [
        {"name": "1. Attention A8KV8  + FFN A4W4 (INT4)", "kv_bits": 8, "kv_fmt": "int", "ffn_fmt": "int"},
        {"name": "2. Attention A8KV8  + FFN A4W4 (FP4) ", "kv_bits": 8, "kv_fmt": "int", "ffn_fmt": "fp"},
        {"name": "3. Attention A8KV4 (INT4) + FFN A4W4 (INT4)", "kv_bits": 4, "kv_fmt": "int", "ffn_fmt": "int"},
        {"name": "4. Attention A8KV4 (FP4)  + FFN A4W4 (FP4) ", "kv_bits": 4, "kv_fmt": "fp", "ffn_fmt": "fp"},
    ]
    
    # Calculate Baseline
    q = "If I have 5 apples and eat 2, how many are left?"
    inputs = tokenizer([tokenizer.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True)], return_tensors="pt")
    
    print("Computing Baseline FP16 for SNR/Cosine Metric...")
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    del model_fp16
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    for cfg in configs:
        print(f"\n======================================")
        print(f"Testing: {cfg['name']}")
        print(f"======================================")
        
        ATTN_KV_BITS = cfg['kv_bits']
        ATTN_KV_FORMAT = cfg['kv_fmt']
        FFN_ACT_FORMAT = cfg['ffn_fmt']
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
        apply_patch(model)
        Qwen2Attention.forward = configurable_attention_forward

        # 1. Evaluate Metrics on a single prompt
        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB")

        # 2. Run 10-Prompt Benchmark
        passed = 0
        for i, q_data in enumerate(QUESTIONS):
            msgs = [{"role": "user", "content": q_data["q"]}]
            txt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            inps = tokenizer([txt], return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inps, max_new_tokens=15, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            ans = tokenizer.decode(out[0][inps.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace('\n', ' ')
            is_pass = evaluate_answer(ans, q_data["keys"])
            if is_pass: passed += 1
            if i < 2: print(f"  Q{i+1} Output: {ans}") # Print first two samples for sanity
            
        print(f"-> Pass Rate: {(passed/len(QUESTIONS))*100:.1f}% ({passed}/{len(QUESTIONS)})")
        
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    run()
