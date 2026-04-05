import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import math
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

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

# Global configuration for target rank ratio (e.g. 0.25 = compress to 25% rank -> 4x compression)
RANK_RATIO = 0.25

def apply_low_rank_approximation(tensor, rank_ratio):
    """
    Simulates storing the KV cache as a low-rank approximation.
    Input: (batch, heads, seq_len, head_dim)
    """
    bsz, heads, seq_len, head_dim = tensor.shape
    
    # We apply SVD on the seq_len x head_dim matrix for each head
    # Flatten batch and heads
    tensor_flat = tensor.view(-1, seq_len, head_dim)
    
    # Target rank
    target_rank = max(1, int(min(seq_len, head_dim) * rank_ratio))
    
    # We must operate in FP32 for SVD stability
    tensor_f32 = tensor_flat.to(torch.float32)
    
    approximated_tensors = []
    
    # In real hardware, we only store U and S*V^T. 
    # For simulation, we reconstruct the matrix immediately to feed it back into PyTorch's eager attention.
    for i in range(tensor_f32.shape[0]):
        matrix = tensor_f32[i]
        try:
            U, S, V = torch.svd(matrix)
            
            # Truncate to target_rank
            U_trunc = U[:, :target_rank]
            S_trunc = S[:target_rank]
            V_trunc = V[:, :target_rank]
            
            # Reconstruct: U * diag(S) * V^T
            approx = torch.matmul(U_trunc * S_trunc.unsqueeze(0), V_trunc.t())
            approximated_tensors.append(approx)
        except Exception:
            # SVD might fail to converge in rare edge cases, fallback to original
            approximated_tensors.append(matrix)
            
    reconstructed = torch.stack(approximated_tensors).view(bsz, heads, seq_len, head_dim)
    return reconstructed.to(tensor.dtype)

ORIGINAL_FORWARD = Qwen2Attention.forward

def low_rank_kv_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
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

    past_kv = past_key_value if past_key_value is not None else past_key_values
    if past_kv is not None:
        cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
        key_states, value_states = past_kv.update(key_states, value_states, self.layer_idx, cache_kwargs)

    # --- THE LOW RANK INJECTION ---
    # In autoregressive generation, we compress the FULL accumulated KV cache history.
    # Real hardware would do this incrementally (like streaming SVD or updating the low-rank bases).
    # Here we do it statically on the full sequence for the mathematical upper-bound simulation.
    
    # We only compress if sequence length is > 1 (makes no sense for single token)
    if key_states.shape[2] > 1:
        key_states_compressed = apply_low_rank_approximation(key_states, rank_ratio=RANK_RATIO)
        value_states_compressed = apply_low_rank_approximation(value_states, rank_ratio=RANK_RATIO)
    else:
        key_states_compressed = key_states
        value_states_compressed = value_states

    import transformers.models.qwen2.modeling_qwen2 as qwen2_mod
    key_states_rep = qwen2_mod.repeat_kv(key_states_compressed, self.config.num_attention_heads // self.config.num_key_value_heads)
    value_states_rep = qwen2_mod.repeat_kv(value_states_compressed, self.config.num_attention_heads // self.config.num_key_value_heads)

    attn_weights = torch.matmul(query_states, key_states_rep.transpose(2, 3)) / math.sqrt(self.head_dim)
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, : key_states_rep.shape[-2]]
        attn_weights = attn_weights + causal_mask

    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=self.config.attention_dropout, training=self.training)

    attn_output = torch.matmul(attn_weights, value_states_rep)
    attn_output = attn_output.transpose(1, 2).contiguous()
    attn_output = attn_output.reshape(bsz, q_len, self.config.hidden_size)
    attn_output = self.o_proj(attn_output)

    if not output_attentions: attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

def run():
    global RANK_RATIO
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    print("Computing Baseline FP16...")
    q = "If I have 5 apples and eat 2, how many are left?"
    inputs = tokenizer([tokenizer.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True)], return_tensors="pt")
    
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    del model_fp16
    torch.cuda.empty_cache()

    configs = [
        {"name": "1. SVD Low-Rank 50% (2x Compression)", "ratio": 0.50},
        {"name": "2. SVD Low-Rank 25% (4x Compression, equivalent to 4-bit)", "ratio": 0.25},
        {"name": "3. SVD Low-Rank 12.5% (8x Compression)", "ratio": 0.125}
    ]

    for cfg in configs:
        print(f"\n==================================================")
        print(f"Testing: {cfg['name']}")
        print(f"==================================================")
        RANK_RATIO = cfg['ratio']
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
        Qwen2Attention.forward = low_rank_kv_forward

        # Metric
        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB")

        # Benchmark
        passed = 0
        for i, q_data in enumerate(QUESTIONS):
            msgs = [{"role": "user", "content": q_data["q"]}]
            txt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            inps = tokenizer([txt], return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inps, max_new_tokens=15, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            ans = tokenizer.decode(out[0][inps.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace('\n', ' ')
            if evaluate_answer(ans, q_data["keys"]): passed += 1
            if i < 2: print(f"  Q{i+1}: {ans}")
            
        print(f"-> Pass Rate: {(passed/len(QUESTIONS))*100:.1f}% ({passed}/{len(QUESTIONS)})")
        
        del model
        torch.cuda.empty_cache()

if __name__ == "__main__":
    run()
