import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
import math
from scipy.linalg import hadamard

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def get_hadamard_matrix(dim, device, dtype):
    h = torch.tensor(hadamard(dim), dtype=dtype, device=device)
    return h / math.sqrt(dim)

def fake_quantize(tensor, bits=4, block_size=None):
    if bits == 4:
        qmin, qmax = -8, 7
    elif bits == 8:
        qmin, qmax = -128, 127
    else:
        return tensor

    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.view(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        dq_tensor = q_tensor * scale
        return dq_tensor.view(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

HADAMARD_MATRICES = {}
ORIGINAL_FORWARD = Qwen2Attention.forward

# --- 1D Feature-Only Hadamard Attention (A4 input, KV4 cache) ---
def a4kv4_1d_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
    # A4 Input to Attention
    hidden_states = fake_quantize(hidden_states, bits=4)
    
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

    # ONLY 1D Hadamard (Feature Dimension)
    if self.head_dim not in HADAMARD_MATRICES:
        HADAMARD_MATRICES[self.head_dim] = get_hadamard_matrix(self.head_dim, query_states.device, query_states.dtype)
    H_feat = HADAMARD_MATRICES[self.head_dim]

    query_states = query_states @ H_feat
    key_states = key_states @ H_feat
    value_states = value_states @ H_feat

    # KV Cache 4-bit Quantization
    key_states = fake_quantize(key_states, bits=4)
    value_states = fake_quantize(value_states, bits=4)

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
    attn_output = attn_output @ H_feat.T

    attn_output = attn_output.transpose(1, 2).contiguous()
    attn_output = attn_output.reshape(bsz, q_len, self.config.hidden_size)
    
    # A4 Input to o_proj
    attn_output = fake_quantize(attn_output, bits=4)
    attn_output = self.o_proj(attn_output)

    if not output_attentions:
        attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

# --- FFN A8W4 (Block 32) ---
class FFN_A8W4_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias

    def forward(self, x):
        w = fake_quantize(self.weight, bits=4, block_size=32)
        x_q = fake_quantize(x, bits=8, block_size=32)
        return F.linear(x_q, w, self.bias)

def apply_a8w4_patch(model):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            if "lm_head" not in name:
                setattr(model, name, FFN_A8W4_Linear(module))
        else:
            apply_a8w4_patch(module)

def run():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    q = "If I have 5 apples and eat 2, how many are left?"
    messages = [{"role": "user", "content": q}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt")

    print("Computing Baseline FP16...")
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    del model_fp16
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    print("\nRunning Config: A4KV4 (1D Hadamard) + FFN A8W4 (Block 32)")
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
    apply_a8w4_patch(model)
    Qwen2Attention.forward = a4kv4_1d_forward

    with torch.no_grad():
        out = model.generate(**inputs.to(model.device), max_new_tokens=20, pad_token_id=tokenizer.eos_token_id, do_sample=False)
        quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
    
    ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip()
    print(f"Output: {ans}")
    
    cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
    rmse = torch.sqrt(F.mse_loss(base_hidden, quant_hidden)).item()
    snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
    
    print(f"Metrics - Cosine: {cos_sim:.4f} | SNR: {snr:.2f} dB | RMSE: {rmse:.4f}")

if __name__ == "__main__":
    run()
