import torch
import torch.nn as nn
import math
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
from transformers.cache_utils import Cache
from typing import Optional, Tuple
from scipy.linalg import hadamard

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def get_hadamard_matrix(dim, device, dtype):
    h = torch.tensor(hadamard(dim), dtype=dtype, device=device)
    return h / math.sqrt(dim)

def fake_quantize_4bit(tensor):
    qmin, qmax = 0, 15
    min_val = tensor.min(dim=-1, keepdim=True)[0]
    max_val = tensor.max(dim=-1, keepdim=True)[0]
    scale = (max_val - min_val) / (qmax - qmin)
    scale = torch.clamp(scale, min=1e-5)
    q_tensor = torch.round((tensor - min_val) / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    return (q_tensor * scale) + min_val

# We will save the original forward
ORIGINAL_FORWARD = Qwen2Attention.forward
HADAMARD_MATRICES = {}

def a4kv4_forward(
    self,
    hidden_states: torch.Tensor,
    attention_mask: Optional[torch.Tensor] = None,
    position_ids: Optional[torch.LongTensor] = None,
    past_key_value: Optional[Cache] = None,
    past_key_values: Optional[Cache] = None,
    output_attentions: bool = False,
    use_cache: bool = False,
    cache_position: Optional[torch.LongTensor] = None,
    position_embeddings: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
):
    # Standard QKV projection
    bsz, q_len, _ = hidden_states.size()

    query_states = self.q_proj(hidden_states)
    key_states = self.k_proj(hidden_states)
    value_states = self.v_proj(hidden_states)

    query_states = query_states.view(bsz, q_len, self.config.num_attention_heads, self.head_dim).transpose(1, 2)
    key_states = key_states.view(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)
    value_states = value_states.view(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)

    # Apply RoPE
    cos, sin = position_embeddings
    from transformers.models.qwen2.modeling_qwen2 import apply_rotary_pos_emb
    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, unsqueeze_dim=1)

    # --- A4KV4 INJECTION START ---
    head_dim = self.head_dim
    if head_dim not in HADAMARD_MATRICES:
        HADAMARD_MATRICES[head_dim] = get_hadamard_matrix(head_dim, query_states.device, query_states.dtype)
    H_feat = HADAMARD_MATRICES[head_dim]

    # 1. Hadamard Transform Features
    query_states = query_states @ H_feat
    key_states = key_states @ H_feat
    value_states = value_states @ H_feat # V also gets transformed if we want uniform processing

    # 2. Fake Quantize K and V to 4-bit (Simulation of the memory footprint reduction)
    key_states = fake_quantize_4bit(key_states)
    value_states = fake_quantize_4bit(value_states)
    # --- A4KV4 INJECTION END ---

    past_kv = past_key_value if past_key_value is not None else past_key_values
    if past_kv is not None:
        cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
        key_states, value_states = past_kv.update(key_states, value_states, self.layer_idx, cache_kwargs)

    # Attention Calculation
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
    
    # Reverse Hadamard on V to restore original space before O_proj
    attn_output = attn_output @ H_feat.T

    if attn_output.size() != (bsz, self.config.num_attention_heads, q_len, self.head_dim):
        raise ValueError(f"`attn_output` should be of size {(bsz, self.config.num_attention_heads, q_len, self.head_dim)}, but is {attn_output.size()}")

    attn_output = attn_output.transpose(1, 2).contiguous()
    attn_output = attn_output.reshape(bsz, q_len, self.config.hidden_size)

    attn_output = self.o_proj(attn_output)

    
    if not output_attentions:
        attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

    
    if not output_attentions:
        attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)
 # This is technically correct, but wait, forward in modeling_qwen2 returns a tuple. Let's return just what it expects.

def run_test():
    print(f"Loading {MODEL_ID} with eager attention...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        torch_dtype=torch.float16, 
        device_map="auto",
        attn_implementation="eager"
    )

    question = "If I have 3 apples and eat 1, how many are left?"
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": question}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # 1. Baseline Run
    print("\n--- Running Baseline FP16 ---")
    start = time.time()
    with torch.no_grad():
        out_base = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id, do_sample=False)
    lat_base = time.time() - start
    ans_base = tokenizer.decode(out_base[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
    print(f"Ans: {ans_base}\nLatency: {lat_base:.2f}s")

    # 2. Patch Attention and Run A4KV4
    print("\n--- Patching Qwen2Attention with A4KV4 (Hadamard + 4-bit) ---")
    Qwen2Attention.forward = a4kv4_forward
    
    start = time.time()
    with torch.no_grad():
        out_quant = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id, do_sample=False)
    lat_quant = time.time() - start
    ans_quant = tokenizer.decode(out_quant[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
    print(f"Ans: {ans_quant}\nLatency: {lat_quant:.2f}s")

if __name__ == "__main__":
    run_test()
