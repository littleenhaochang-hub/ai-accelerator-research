import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import math
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# 10 Diverse Prompts for rapid evaluation
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

# --- Quantization Formats ---
def quantize_int4(tensor, block_size=None):
    """Uniform INT4 (-8 to 7)"""
    qmin, qmax = -8, 7
    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.reshape(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return (q_tensor * scale).reshape(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

def quantize_fp4_e2m1(tensor, block_size=None):
    """
    OCP FP4 (E2M1) Format: 1 sign, 2 exp, 1 mantissa.
    Positive Representable Values (normalized to max=6.0 for symmetric scaling):
    0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0
    
    Why this matters: INT4 has values like 1, 2, 3, 4, 5, 6, 7. 
    FP4 has ultra-dense resolution near zero (0.5, 1.0, 1.5), perfectly 
    matching the bell-curve distribution of neural network activations.
    """
    fp4_levels = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], device=tensor.device, dtype=tensor.dtype)
    orig_shape = tensor.shape
    
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.reshape(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        
        # In FP4, the maximum representable value is 6.0
        scale = max_val / 6.0
        scale = torch.clamp(scale, min=1e-5)
        
        normalized = torch.abs(tensor_blocked) / scale
        
        # Nearest neighbor mapping to FP4 levels
        diffs = torch.abs(normalized.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        
        # Restore sign and scale
        return (torch.sign(tensor_blocked) * quantized_abs * scale).reshape(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / 6.0
        scale = torch.clamp(scale, min=1e-5)
        
        normalized = torch.abs(tensor) / scale
        diffs = torch.abs(normalized.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        return torch.sign(tensor) * quantized_abs * scale

# --- Custom Linear Layer for Data Type Ablation ---
class DataTypeLinear(nn.Module):
    def __init__(self, original_linear, data_type="fp4", block_size=None):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.data_type = data_type
        self.block_size = block_size

    def forward(self, x):
        if self.data_type == "fp4":
            w = quantize_fp4_e2m1(self.weight, block_size=self.block_size)
            x_q = quantize_fp4_e2m1(x, block_size=self.block_size)
        elif self.data_type == "int4":
            w = quantize_int4(self.weight, block_size=self.block_size)
            x_q = quantize_int4(x, block_size=self.block_size)
        else: # baseline
            w = self.weight
            x_q = x
            
        return F.linear(x_q, w, self.bias)

def apply_patch(model, data_type, block_size):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "lm_head" not in name:
            setattr(model, name, DataTypeLinear(module, data_type, block_size))
        else:
            apply_patch(module, data_type, block_size)

def run():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    q = "If I have 5 apples and eat 2, how many are left?"
    inputs = tokenizer([tokenizer.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True)], return_tensors="pt")
    
    print("Computing Baseline FP16 (No Quantization)...")
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    del model_fp16
    torch.cuda.empty_cache()

    # The Ultimate Data Type Showdown
    configs = [
        {"name": "1. INT4 (Block 32) [Control Group]", "dtype": "int4", "blk": 32},
        {"name": "2. FP4  (Block 32) [OCP Target]", "dtype": "fp4", "blk": 32},
        {"name": "3. INT4 (No Block 32 - Pure Uniform)", "dtype": "int4", "blk": None},
        {"name": "4. FP4  (No Block 32 - Pure E2M1)", "dtype": "fp4", "blk": None},
    ]

    for cfg in configs:
        print(f"\n==================================================")
        print(f"Testing: {cfg['name']}")
        print(f"==================================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        
        # Apply the W4A4 patch to ALL Linear layers (Attention QKVO + FFN)
        apply_patch(model, data_type=cfg["dtype"], block_size=cfg["blk"])

        # Metric Evaluation
        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
        
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        rmse = torch.sqrt(F.mse_loss(base_hidden, quant_hidden)).item()
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB | RMSE: {rmse:.4f}")

        # Benchmark 10 Prompts
        passed = 0
        for i, q_data in enumerate(QUESTIONS):
            msgs = [{"role": "user", "content": q_data["q"]}]
            txt = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            inps = tokenizer([txt], return_tensors="pt").to(model.device)
            with torch.no_grad():
                out = model.generate(**inps, max_new_tokens=15, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            ans = tokenizer.decode(out[0][inps.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace('\n', ' ')
            if evaluate_answer(ans, q_data["keys"]): passed += 1
            if i < 2: print(f"  Q{i+1}: {ans[:60]}...")
            
        print(f"-> Pass Rate: {(passed/len(QUESTIONS))*100:.1f}% ({passed}/{len(QUESTIONS)})")
        
        del model
        torch.cuda.empty_cache()

if __name__ == "__main__":
    run()
