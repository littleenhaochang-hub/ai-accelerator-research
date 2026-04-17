import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from ppl_evaluator import evaluate_ppl

class RoundWithSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        return torch.round(x)

    @staticmethod
    def backward(ctx, grad_output):
        return grad_output

def ternary_quantize_with_ste(weight):
    scale = weight.abs().mean().clamp(min=1e-5)
    scaled_weight = weight / scale
    quantized_weight = torch.clamp(RoundWithSTE.apply(scaled_weight), min=-1.0, max=1.0)
    return quantized_weight * scale

def apply_ternary_ptq(model):
    print("Applying Zero-Shot Ternary PTQ (W1.58) to all Linear layers...")
    quantized_layers = 0
    with torch.no_grad():
        for name, module in model.named_modules():
            if isinstance(module, nn.Linear) and "lm_head" not in name:
                module.weight.data = ternary_quantize_with_ste(module.weight.data).to(module.weight.dtype)
                quantized_layers += 1
    print(f"Quantized {quantized_layers} linear layers to Ternary.")

if __name__ == "__main__":
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model_id = "google/gemma-3-270m"
    cache_dir = "/Users/hao/.openclaw/workspace/offload_tmp/huggingface"
    
    token = None
    env_path = "/Users/hao/.openclaw/workspace/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("HF_TOKEN="): 
                    token = line.split("=")[1].strip()
                    break

    print(f"Loading {model_id} for Full-Model Ternary PTQ Test...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        low_cpu_mem_usage=True, 
        token=token, 
        cache_dir=cache_dir
    ).to(device)

    # Apply PTQ
    apply_ternary_ptq(model)
    
    # Evaluate PPL
    ptq_ppl = evaluate_ppl(model, tokenizer, sequence_length=1024)
    print(f"[PTQ Verdict] Full-Model W1.58 PPL: {ptq_ppl:.4f}")
