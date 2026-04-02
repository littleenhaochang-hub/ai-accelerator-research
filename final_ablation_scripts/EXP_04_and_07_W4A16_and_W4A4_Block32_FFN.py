import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def fake_quantize(tensor, bits=4, group_size=None):
    """Fake quantization with optional group-wise scaling."""
    qmin, qmax = -8, 7

    if group_size is not None and tensor.shape[-1] % group_size == 0:
        # Group-wise quantization along the last dimension
        orig_shape = tensor.shape
        tensor = tensor.view(-1, group_size)
        scale = (tensor.max(dim=-1, keepdim=True)[0] - tensor.min(dim=-1, keepdim=True)[0]) / (qmax - qmin)
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        dq_tensor = q_tensor * scale
        return dq_tensor.view(orig_shape)
    else:
        # Per-tensor or per-channel (if 2D)
        scale = (tensor.max(dim=-1, keepdim=True)[0] - tensor.min(dim=-1, keepdim=True)[0]) / (qmax - qmin)
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

def block_micro_scaling_quantize(tensor, block_size=32):
    """
    Sub-vector Micro-Scaling (similar to NVIDIA MX4 / OCP FP4 specs).
    Every block of 32 elements gets its own FP16 scale.
    """
    # Reshape tensor to isolate blocks of size 32
    orig_shape = tensor.shape
    # If the last dimension is not divisible by block_size, pad or fallback
    if tensor.shape[-1] % block_size != 0:
        return fake_quantize(tensor, bits=4)
        
    tensor_blocked = tensor.view(-1, block_size)
    
    # Calculate scale per block of 32
    qmin, qmax = -8, 7
    # Use max absolute value for symmetric quantization within the block
    max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
    scale = max_val / qmax
    scale = torch.clamp(scale, min=1e-5)
    
    # Quantize to 4-bit
    q_tensor = torch.round(tensor_blocked / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    
    # Dequantize back to FP16 space
    dq_tensor = q_tensor * scale
    
    return dq_tensor.view(orig_shape)

class Block32AblationLinear(nn.Module):
    def __init__(self, original_linear, apply_to_act=True):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.apply_to_act = apply_to_act

    def forward(self, x):
        # Weights are always block32 quantized
        w = block_micro_scaling_quantize(self.weight, block_size=32)
        
        # Activations
        if self.apply_to_act:
            x_q = block_micro_scaling_quantize(x, block_size=32)
        else:
            x_q = x
            
        return F.linear(x_q, w, self.bias)

def replace_linear_layers(model, apply_to_act=True):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            if "lm_head" not in name:
                setattr(model, name, Block32AblationLinear(module, apply_to_act))
        else:
            replace_linear_layers(module, apply_to_act)

def run_ablation():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    question = "If I have 3 apples and eat 1, how many are left?"
    
    configs = [
        {"name": "1. W4A16 (Block32 on Weights ONLY)", "act": False},
        {"name": "2. W4A4 (Block32 Micro-Scaling on BOTH)", "act": True},
    ]
    
    for cfg in configs:
        print(f"\n======================================")
        print(f"Testing Strategy: {cfg['name']}")
        print(f"======================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        replace_linear_layers(model, apply_to_act=cfg['act'])
            
        messages = [{"role": "user", "content": question}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        start = time.time()
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id, do_sample=False)
        latency = time.time() - start
        
        ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace("\n", " ")
        print(f"Ans: {ans}")
        print(f"Lat: {latency:.2f}s")
        
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    run_ablation()
