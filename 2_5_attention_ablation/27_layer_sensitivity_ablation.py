import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import math

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

def fake_quantize_int4(tensor, block_size=32):
    qmin, qmax = -8, 7
    orig_shape = tensor.shape
    if tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.view(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        dq = (q_tensor * scale).view(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        dq = q_tensor * scale
    
    # Cast back to original dtype to prevent MPS matrix mult crashes
    return dq.to(tensor.dtype)

class W4A4_Block32_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias

    def forward(self, x):
        w = fake_quantize_int4(self.weight, block_size=32)
        x_q = fake_quantize_int4(x, block_size=32)
        return F.linear(x_q, w, self.bias)

def apply_mixed_precision_patch(model, condition_fn, prefix=""):
    for name, module in model.named_children():
        full_name = f"{prefix}.{name}" if prefix else name
        if isinstance(module, nn.Linear):
            if "lm_head" not in full_name and condition_fn(full_name):
                setattr(model, name, W4A4_Block32_Linear(module))
        else:
            apply_mixed_precision_patch(module, condition_fn, prefix=full_name)

def run():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    print("Computing Baseline FP16...")
    q = "If I have 5 apples and eat 2, how many are left?"
    inputs = tokenizer([tokenizer.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True)], return_tensors="pt")
    
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    NUM_LAYERS = model_fp16.config.num_hidden_layers
    del model_fp16
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # Define Sensitivity Strategies
    configs = [
        {
            "name": "1. All Layers W4A4 (Baseline)",
            "cond": lambda name: True
        },
        {
            "name": "2. Skip First & Last Layer (Quantize mid layers)",
            "cond": lambda name: not (f"model.layers.0." in name or f"model.layers.{NUM_LAYERS-1}." in name)
        },
        {
            "name": "3. Attention Only W4A4 (FFN is FP16)",
            "cond": lambda name: "self_attn" in name
        },
        {
            "name": "4. FFN Only W4A4 (Attention is FP16)",
            "cond": lambda name: "mlp" in name
        },
        {
            "name": "5. Late Layers Only W4A4 (Quantize layer 12-23)",
            "cond": lambda name: any(f"model.layers.{i}." in name for i in range(NUM_LAYERS//2, NUM_LAYERS))
        }
    ]

    for cfg in configs:
        print(f"\n======================================")
        print(f"Testing: {cfg['name']}")
        print(f"======================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        
        # Apply selective patching
        apply_mixed_precision_patch(model, cfg["cond"])

        # 1. Metric evaluation
        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB")

        # 2. Benchmark
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
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    run()
