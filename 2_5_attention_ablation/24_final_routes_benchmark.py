import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
import math
from scipy.linalg import hadamard

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# --- 20 Diverse Prompts ---
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

def evaluate_answer(ans, keys):
    ans_lower = ans.lower()
    for k in keys:
        if k.lower() in ans_lower: return True
    return False

def get_hadamard_matrix(dim, device, dtype):
    h = torch.tensor(hadamard(dim), dtype=dtype, device=device)
    return h / math.sqrt(dim)

def fake_quantize(tensor, bits=4, block_size=None):
    if bits == 4: qmin, qmax = -8, 7
    else: return tensor

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

# --- Route A: 1D Hadamard A4KV4 Attention ---
def route_a_attention_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
    hidden_states = fake_quantize(hidden_states, bits=4) # A4 input
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
    attn_output = fake_quantize(attn_output, bits=4) # A4 output
    attn_output = self.o_proj(attn_output)

    if not output_attentions: attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

# --- FFN W4A16 (For Route A) ---
class FFN_W4A16_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features, self.out_features = original_linear.in_features, original_linear.out_features
        self.weight, self.bias = original_linear.weight, original_linear.bias
    def forward(self, x):
        w = fake_quantize(self.weight, bits=4, block_size=32)
        return F.linear(x, w, self.bias)

# --- FFN W4A4 Block 32 (For Route B) ---
class FFN_W4A4_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features, self.out_features = original_linear.in_features, original_linear.out_features
        self.weight, self.bias = original_linear.weight, original_linear.bias
    def forward(self, x):
        w = fake_quantize(self.weight, bits=4, block_size=32)
        x_q = fake_quantize(x, bits=4, block_size=32)
        return F.linear(x_q, w, self.bias)

def apply_patch(model, route):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "lm_head" not in name:
            if route == "A": setattr(model, name, FFN_W4A16_Linear(module))
            elif route == "B": setattr(model, name, FFN_W4A4_Linear(module))
        else: apply_patch(module, route)

def run():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    configs = [
        {"name": "Route A (Memory Bound): A4KV4 Attention + FFN W4A16", "route": "A"},
        {"name": "Route B (Compute Bound): Baseline KV16 Attention + FFN W4A4 (Block 32)", "route": "B"}
    ]
    
    for cfg in configs:
        print(f"\nEvaluating: {cfg['name']}")
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto", attn_implementation="eager")
        
        apply_patch(model, cfg['route'])
        if cfg['route'] == "A":
            Qwen2Attention.forward = route_a_attention_forward
        else:
            Qwen2Attention.forward = ORIGINAL_FORWARD

        passed = 0
        for i, q_data in enumerate(QUESTIONS):
            messages = [{"role": "user", "content": q_data["q"]}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([text], return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace('\n', ' ')
            is_pass = evaluate_answer(ans, q_data["keys"])
            if is_pass: passed += 1
            
        print(f"-> Pass Rate: {(passed/20)*100:.1f}% ({passed}/20)")
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    run()
