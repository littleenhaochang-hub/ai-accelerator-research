import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
import math

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def apply_scale_format(scale, format_type):
    """
    Simulates various hardware scale factor formats.
    """
    if format_type == "fp16":
        return scale
        
    elif format_type == "e8m0":
        # Pure exponent shift. 8 bits for exponent, 0 for mantissa.
        # This is a power of 2 constraint: Scale = 2^E
        exponent = torch.round(torch.log2(scale + 1e-9))
        return 2.0 ** exponent
        
    elif format_type == "e4m3":
        # Standard FP8 for ML (4 exponent, 3 mantissa)
        exponent = torch.floor(torch.log2(scale + 1e-9))
        exponent = torch.clamp(exponent, min=-7, max=8)
        normalized = scale / (2.0 ** exponent)
        mantissa = normalized - 1.0
        # 3 mantissa bits -> 8 levels
        rounded_mantissa = torch.round(mantissa * 8.0) / 8.0
        return (2.0 ** exponent) * (1.0 + rounded_mantissa)
        
    elif format_type == "e3m4":
        # Alternative FP8 (3 exponent, 4 mantissa)
        exponent = torch.floor(torch.log2(scale + 1e-9))
        exponent = torch.clamp(exponent, min=-3, max=4)
        normalized = scale / (2.0 ** exponent)
        mantissa = normalized - 1.0
        # 4 mantissa bits -> 16 levels
        rounded_mantissa = torch.round(mantissa * 16.0) / 16.0
        return (2.0 ** exponent) * (1.0 + rounded_mantissa)
        
    return scale

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
        
        # Apply Hardware Scale Constraint
        scale = apply_scale_format(scale, scale_format)
        
        normalized = torch.abs(tensor_blocked) / scale
        
        diffs = torch.abs(normalized.unsqueeze(-1) - fp4_levels)
        idx = torch.argmin(diffs, dim=-1)
        quantized_abs = fp4_levels[idx]
        
        return (torch.sign(tensor_blocked) * quantized_abs * scale).reshape(orig_shape)
    else:
        return tensor

class ScaleComparisonLinear(nn.Module):
    def __init__(self, original_linear, scale_fmt):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.scale_fmt = scale_fmt

    def forward(self, x):
        # Block 32 FP4 for both weight and activation
        w = quantize_fp4_e2m1(self.weight, block_size=32, scale_format=self.scale_fmt)
        x_q = quantize_fp4_e2m1(x, block_size=32, scale_format=self.scale_fmt)
        return F.linear(x_q, w, self.bias)

def apply_patch(model, scale_fmt):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "lm_head" not in name:
            setattr(model, name, ScaleComparisonLinear(module, scale_fmt))
        else:
            apply_patch(module, scale_fmt)

def run():
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
        {"name": "1. FP16 Scale (Baseline: 4.50 bits)", "sfmt": "fp16"},
        {"name": "2. E4M3 Scale (FP8: 4.25 bits)", "sfmt": "e4m3"},
        {"name": "3. E3M4 Scale (FP8: 4.25 bits)", "sfmt": "e3m4"},
        {"name": "4. E8M0 Scale (Multiplier-Free: 4.25 bits)", "sfmt": "e8m0"},
    ]

    for cfg in configs:
        print(f"\n==================================================")
        print(f"Testing: {cfg['name']}")
        print(f"==================================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        apply_patch(model, scale_fmt=cfg["sfmt"])

        with torch.no_grad():
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
            
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        rmse = torch.sqrt(F.mse_loss(base_hidden, quant_hidden)).item()
        
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB | RMSE: {rmse:.4f}")
        
        del model
        torch.cuda.empty_cache()

if __name__ == "__main__":
    run()
