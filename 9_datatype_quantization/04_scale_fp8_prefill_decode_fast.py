import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
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

def apply_fp8_scale(scale, format_type):
    """
    Simulates FP8 scale quantization.
    FP16 has 5 exponent bits, 10 mantissa bits.
    E4M3 (Standard FP8 for deep learning weights): 4 exponent bits, 3 mantissa bits.
    E3M4 (Alternative FP8): 3 exponent bits, 4 mantissa bits.
    We approximate the loss of precision by rounding the mantissa and clamping the exponent range.
    """
    if format_type == "fp16":
        return scale
        
    # We are dealing with positive scale factors only.
    # A simple simulation:
    # 1. Extract exponent (base 2)
    exponent = torch.floor(torch.log2(scale + 1e-9))
    
    # 2. Clamp exponent based on bits
    if format_type == "e4m3":
        # 4 bits for exponent -> 15 values -> roughly -7 to +8
        exponent = torch.clamp(exponent, min=-7, max=8)
        mantissa_bits = 3
    elif format_type == "e3m4":
        # 3 bits for exponent -> 7 values -> roughly -3 to +4
        exponent = torch.clamp(exponent, min=-3, max=4)
        mantissa_bits = 4
    else:
        return scale
        
    # 3. Extract and round mantissa
    # Scale = 2^E * (1 + M) -> M = (Scale / 2^E) - 1
    normalized = scale / (2.0 ** exponent)
    mantissa = normalized - 1.0
    
    # Round mantissa to available bits (2^mantissa_bits levels)
    mantissa_levels = 2 ** mantissa_bits
    rounded_mantissa = torch.round(mantissa * mantissa_levels) / mantissa_levels
    
    # 4. Reconstruct scale
    q_scale = (2.0 ** exponent) * (1.0 + rounded_mantissa)
    return q_scale

def quantize_fp4_e2m1(tensor, block_size=32, scale_format="fp16"):
    """OCP FP4 (E2M1) Format with configurable Scale Precision"""
    fp4_levels = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], device=tensor.device, dtype=tensor.dtype)
    orig_shape = tensor.shape
    
    if tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.reshape(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        
        # Base scale
        scale = max_val / 6.0
        scale = torch.clamp(scale, min=1e-5)
        
        # Apply Hardware Scale Constraint (FP8 E4M3 or E3M4)
        scale = apply_fp8_scale(scale, scale_format)
        
        normalized = torch.abs(tensor_blocked) / scale
        
        diffs = torch.abs(normalized.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        
        return (torch.sign(tensor_blocked) * quantized_abs * scale).reshape(orig_shape)
    else:
        return tensor

# Global configs for phases
PREFILL_SCALE_FMT = "fp16"
DECODE_SCALE_FMT = "fp16"

class PhaseAwareFP4Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias

    def forward(self, x):
        # Determine if we are in Prefill (seq_len > 1) or Decode (seq_len == 1) phase
        # x shape is (batch, seq_len, hidden_dim)
        seq_len = x.shape[1]
        current_phase_scale_fmt = PREFILL_SCALE_FMT if seq_len > 1 else DECODE_SCALE_FMT
        
        # Quantize weight with the phase's scale format constraint
        w = quantize_fp4_e2m1(self.weight, block_size=32, scale_format=current_phase_scale_fmt)
        
        # Quantize activation with the phase's scale format constraint
        x_q = quantize_fp4_e2m1(x, block_size=32, scale_format=current_phase_scale_fmt)
        
        return F.linear(x_q, w, self.bias)

def apply_patch(model):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "lm_head" not in name:
            setattr(model, name, PhaseAwareFP4Linear(module))
        else:
            apply_patch(module)

def run():
    global PREFILL_SCALE_FMT, DECODE_SCALE_FMT
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    q = "If I have 5 apples and eat 2, how many are left?"
    inputs = tokenizer([tokenizer.apply_chat_template([{"role": "user", "content": q}], tokenize=False, add_generation_prompt=True)], return_tensors="pt")
    
    print("Computing Baseline FP16...")
    model_fp16 = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    with torch.no_grad():
        base_hidden = model_fp16(inputs.input_ids.to(model_fp16.device), output_hidden_states=True).hidden_states[-1]
    del model_fp16
    torch.cuda.empty_cache()

    configs = [
        {"name": "1. Uniform FP16 Scales (Control 4.5 bits)", "prefill": "fp16", "decode": "fp16"},
        {"name": "2. Uniform E4M3 Scales (FP8 Dynamic Range) [4.25 bits]", "prefill": "e4m3", "decode": "e4m3"},
        {"name": "3. Uniform E3M4 Scales (FP8 Precision) [4.25 bits]", "prefill": "e3m4", "decode": "e3m4"},
        {"name": "4. Asymmetric Phases: Prefill FP16 / Decode E4M3", "prefill": "fp16", "decode": "e4m3"},
        {"name": "5. Asymmetric Phases: Prefill E4M3 / Decode E3M4", "prefill": "e4m3", "decode": "e3m4"},
    ]

    for cfg in configs:
        print(f"\n==================================================")
        print(f"Testing: {cfg['name']}")
        print(f"==================================================")
        PREFILL_SCALE_FMT = cfg['prefill']
        DECODE_SCALE_FMT = cfg['decode']
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        apply_patch(model)

        # Metric Evaluation (This only tests the Prefill phase, as seq_len > 1)
        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
            
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        rmse = torch.sqrt(F.mse_loss(base_hidden, quant_hidden)).item()
        print(f"[Prefill Phase] Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB | RMSE: {rmse:.4f}")

        # Benchmark 10 Prompts (Tests both Prefill and sequential Decode phases)
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
