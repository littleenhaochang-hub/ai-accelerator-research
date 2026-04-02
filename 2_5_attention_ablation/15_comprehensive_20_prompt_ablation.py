import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
from transformers.cache_utils import Cache
from typing import Optional, Tuple
from scipy.linalg import hadamard
import math

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# --- 20 Diverse Prompts & Evaluation Keywords ---
QUESTIONS = [
    {"q": "If I have 5 apples and eat 2, how many are left?", "keys": ["3", "three"]},
    {"q": "What is 15 plus 27?", "keys": ["42"]},
    {"q": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?", "keys": ["5", "0.05", "five"]},
    {"q": "Solve for x: 2x + 6 = 14", "keys": ["4", "four"]},
    {"q": "What is the capital of Japan?", "keys": ["Tokyo"]},
    {"q": "Who wrote the play 'Hamlet'?", "keys": ["Shakespeare"]},
    {"q": "What is the chemical symbol for water?", "keys": ["H2O", "h2o"]},
    {"q": "Which planet is known as the Red Planet?", "keys": ["Mars"]},
    {"q": "In what year did the Titanic sink?", "keys": ["1912"]},
    {"q": "Write a Python function 'add' to add two numbers.", "keys": ["def", "return", "add"]},
    {"q": "What does HTML stand for?", "keys": ["Hypertext", "Markup", "Language", "HyperText"]},
    {"q": "List three primary colors.", "keys": ["red", "blue", "yellow", "Red", "Blue", "Yellow"]},
    {"q": "Translate 'Hello, world' into French.", "keys": ["Bonjour", "bonjour", "monde"]},
    {"q": "What is the opposite of the word 'hot'?", "keys": ["cold", "Cold"]},
    {"q": "What is 10 multiplied by 5?", "keys": ["50", "fifty"]},
    {"q": "If tomorrow is Tuesday, what day was yesterday?", "keys": ["Sunday"]},
    {"q": "Name a large grey animal with a trunk.", "keys": ["elephant", "Elephant"]},
    {"q": "Is a tomato a fruit or a vegetable botanically?", "keys": ["fruit", "Fruit"]},
    {"q": "How many continents are there on Earth?", "keys": ["7", "seven", "Seven"]},
    {"q": "Why is the sky blue? Explain in 3 words.", "keys": ["scattering", "Rayleigh", "light", "atmosphere", "blue", "scattered", "sunlight"]}
]

# --- A4KV4 (Attention) Patch ---
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

# --- W4A4 Block32 (FFN/Linear) Patch ---
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

# --- Evaluation Runner ---
def evaluate_answer(ans, keys):
    # Very loose keyword evaluation. If any keyword is in the response, pass.
    ans_lower = ans.lower()
    for k in keys:
        if k.lower() in ans_lower:
            return True
    return False

def run_tests():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    configs = [
        {"id": "Baseline", "name": "1. Baseline (FP16)", "a4kv4": False, "w4a4": False},
        {"id": "A4KV4", "name": "2. A4KV4 Only (Attention Hadamard)", "a4kv4": True, "w4a4": False},
        {"id": "W4A4", "name": "3. W4A4 Only (FFN Block32)", "a4kv4": False, "w4a4": True},
        {"id": "All_4bit", "name": "4. All 4-bit (A4KV4 + W4A4_Block32)", "a4kv4": True, "w4a4": True},
    ]
    
    full_results = []
    summary_data = []

    for cfg in configs:
        print(f"\n[{cfg['name']}] Loading model...")
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
        
        # Apply patches
        if cfg['w4a4']:
            apply_block32_patch(model)
        
        if cfg['a4kv4']:
            Qwen2Attention.forward = a4kv4_forward
        else:
            Qwen2Attention.forward = ORIGINAL_FORWARD

        passed = 0
        config_log = []
        start_cfg_time = time.time()
        
        for i, q_data in enumerate(QUESTIONS):
            q = q_data["q"]
            keys = q_data["keys"]
            
            messages = [{"role": "user", "content": q}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([text], return_tensors="pt").to(model.device)
            
            out = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace("\n", " ")
            
            is_pass = evaluate_answer(ans, keys)
            if is_pass: passed += 1
                
            config_log.append({
                "q_id": i+1,
                "question": q,
                "output": ans,
                "pass": is_pass
            })
            print(f"  Q{i+1}: {'PASS' if is_pass else 'FAIL'} | {ans[:60]}...")
            
        pass_rate = (passed / len(QUESTIONS)) * 100
        latency = time.time() - start_cfg_time
        print(f"-> Pass Rate: {pass_rate}% | Latency: {latency:.2f}s")
        
        summary_data.append({
            "config": cfg['id'],
            "pass_rate": pass_rate,
            "latency": latency
        })
        
        full_results.append({
            "config": cfg['name'],
            "pass_rate": pass_rate,
            "latency": latency,
            "logs": config_log
        })
        
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # Write output JSON
    with open("ai-accelerator-research/reports/comprehensive_20_prompt_results.json", "w") as f:
        json.dump(full_results, f, indent=2)

    # Write Markdown
    md_lines = ["# 20-Prompt Ablation Test Results (Attention + FFN)\n"]
    md_lines.append("## Summary Table\n")
    md_lines.append("| Configuration | Pass Rate | Total Inference Time |\n| :--- | :--- | :--- |\n")
    for s in summary_data:
        md_lines.append(f"| {s['config']} | {s['pass_rate']}% | {s['latency']:.2f}s |\n")
        
    md_lines.append("\n## Detailed Logs\n")
    for res in full_results:
        md_lines.append(f"### {res['config']}\n")
        for log in res['logs']:
            status = "🟢 PASS" if log['pass'] else "🔴 FAIL"
            md_lines.append(f"- **Q{log['q_id']}:** {log['question']}\n  - **Out:** `{log['output']}`\n  - **Eval:** {status}\n")
            
    with open("ai-accelerator-research/reports/comprehensive_20_prompt_results.md", "w") as f:
        f.writelines(md_lines)
        
    print("\nSaved JSON and MD reports to ai-accelerator-research/reports/")

if __name__ == "__main__":
    run_tests()
