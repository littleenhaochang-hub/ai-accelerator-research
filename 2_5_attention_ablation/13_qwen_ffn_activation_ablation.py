import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def fake_quantize(tensor, bits=4, group_size=None, is_activation=False):
    """Fake quantization with optional group-wise scaling."""
    if bits == 4:
        qmin, qmax = -8, 7
    elif bits == 8:
        qmin, qmax = -128, 127
    else:
        return tensor

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

def outlier_aware_fake_quantize(tensor, threshold=6.0):
    """LLM.int8() style: Keep extreme outliers in FP16, quantize the rest to 4-bit."""
    # Find outlier indices based on magnitude
    abs_tensor = torch.abs(tensor)
    outlier_mask = abs_tensor > threshold
    
    # Separate outliers and normal values
    normal_tensor = tensor.clone()
    normal_tensor[outlier_mask] = 0.0 # Zero out outliers for quantization calculation
    
    # Quantize only the normal part to 4-bit
    qmin, qmax = -8, 7
    scale = (normal_tensor.max(dim=-1, keepdim=True)[0] - normal_tensor.min(dim=-1, keepdim=True)[0]) / (qmax - qmin)
    scale = torch.clamp(scale, min=1e-5)
    
    q_tensor = torch.round(normal_tensor / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    dq_tensor = q_tensor * scale
    
    # Restore FP16 outliers perfectly
    dq_tensor[outlier_mask] = tensor[outlier_mask]
    return dq_tensor

class FFNActivationAblationLinear(nn.Module):
    def __init__(self, original_linear, strategy):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.strategy = strategy

    def forward(self, x):
        # Always quantize weights to 4-bit for this test (W4 baseline)
        w = fake_quantize(self.weight, bits=4, group_size=128)
        
        # Apply specific activation quantization strategy
        if self.strategy == "A8":
            x_q = fake_quantize(x, bits=8, is_activation=True)
        elif self.strategy == "A4_Grouped":
            x_q = fake_quantize(x, bits=4, group_size=64, is_activation=True)
        elif self.strategy == "A4_Outlier_Aware":
            x_q = outlier_aware_fake_quantize(x, threshold=6.0) # LLM.int8() style
        else:
            x_q = x # Fallback FP16
            
        return F.linear(x_q, w, self.bias)

def replace_linear_layers(model, strategy):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            if "lm_head" not in name:
                setattr(model, name, FFNActivationAblationLinear(module, strategy))
        else:
            replace_linear_layers(module, strategy)

def run_ablation():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    question = "If I have 3 apples and eat 1, how many are left?"
    
    strategies = [
        {"name": "1. W4A8 (INT8 Activations)", "strategy": "A8"},
        {"name": "2. W4A4 Grouped (GroupSize=64)", "strategy": "A4_Grouped"},
        {"name": "3. W4A4 Outlier-Aware (Top X in FP16, rest A4)", "strategy": "A4_Outlier_Aware"},
    ]
    
    for cfg in strategies:
        print(f"\n======================================")
        print(f"Testing Strategy: {cfg['name']}")
        print(f"======================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        replace_linear_layers(model, cfg['strategy'])
            
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
