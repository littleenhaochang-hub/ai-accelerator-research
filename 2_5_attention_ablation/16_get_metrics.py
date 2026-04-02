import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
import math
from scipy.linalg import hadamard

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# --- Patching Functions (same as before) ---
def get_hadamard_matrix(dim, device, dtype):
    h = torch.tensor(hadamard(dim), dtype=dtype, device=device)
    return h / math.sqrt(dim)

def fake_quantize_4bit_kv(tensor):
    qmin, qmax = -8, 7
    min_val = tensor.min(dim=-1, keepdim=True)[0]
    max_val = tensor.max(dim=-1, keepdim=True)[0]
    scale = (max_val - min_val) / (qmax - qmin)
    scale = torch.clamp(scale, min=1e-5)
    q_tensor = torch.round((tensor - min_val) / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    return (q_tensor * scale) + min_val

HADAMARD_MATRICES = {}
ORIGINAL_FORWARD = Qwen2Attention.forward

def a4kv4_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
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

    if self.head_dim not in HADAMARD_MATRICES:
        HADAMARD_MATRICES[self.head_dim] = get_hadamard_matrix(self.head_dim, query_states.device, query_states.dtype)
    H_feat = HADAMARD_MATRICES[self.head_dim]

    query_states = query_states @ H_feat
    key_states = key_states @ H_feat
    value_states = value_states @ H_feat

    key_states = fake_quantize_4bit_kv(key_states)
    value_states = fake_quantize_4bit_kv(value_states)

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
    attn_output = self.o_proj(attn_output)

    if not output_attentions:
        attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

def block_micro_scaling_quantize(tensor, block_size=32):
    qmin, qmax = -8, 7
    orig_shape = tensor.shape
    if tensor.shape[-1] % block_size != 0:
        return tensor
    tensor_blocked = tensor.view(-1, block_size)
    max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
    scale = max_val / qmax
    scale = torch.clamp(scale, min=1e-5)
    q_tensor = torch.round(tensor_blocked / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    dq_tensor = q_tensor * scale
    return dq_tensor.view(orig_shape)

class Block32Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias

    def forward(self, x):
        w = block_micro_scaling_quantize(self.weight, block_size=32)
        x_q = block_micro_scaling_quantize(x, block_size=32)
        return F.linear(x_q, w, self.bias)

def apply_block32_patch(model):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            if "lm_head" not in name:
                setattr(model, name, Block32Linear(module))
        else:
            apply_block32_patch(module)

# --- Compute Metrics ---
def compute_metrics():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    q = "If I have 5 apples and eat 2, how many are left?"
    messages = [{"role": "user", "content": q}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt")

    # 1. Get Baseline Hidden States (before lm_head)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
    with torch.no_grad():
        base_out = model(inputs.input_ids.to(model.device), output_hidden_states=True)
        base_hidden = base_out.hidden_states[-1] # Last layer hidden state
    del model
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    configs = [
        {"name": "2. W4A4 (Block 32)", "a4kv4": False, "w4a4": True},
        {"name": "3. A4KV4 Only", "a4kv4": True, "w4a4": False},
        {"name": "4. All 4-bit Extreme", "a4kv4": True, "w4a4": True},
    ]

    print(f"Metrics against Baseline FP16 (Token Sequence length: {base_hidden.shape[1]})")
    for cfg in configs:
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
        if cfg['w4a4']: apply_block32_patch(model)
        if cfg['a4kv4']: Qwen2Attention.forward = a4kv4_forward
        
        with torch.no_grad():
            quant_out = model(inputs.input_ids.to(model.device), output_hidden_states=True)
            quant_hidden = quant_out.hidden_states[-1]
            
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        rmse = torch.sqrt(F.mse_loss(base_hidden, quant_hidden)).item()
        
        # SNR = 10 * log10( sum(base^2) / sum((base-quant)^2) )
        signal_power = torch.mean(base_hidden**2)
        noise_power = torch.mean((base_hidden - quant_hidden)**2)
        snr = 10 * torch.log10(signal_power / noise_power).item()
        
        print(f"{cfg['name']}:")
        print(f"  Cosine Sim: {cos_sim:.4f}")
        print(f"  RMSE:       {rmse:.4f}")
        print(f"  SNR:        {snr:.2f} dB")
        
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    compute_metrics()
