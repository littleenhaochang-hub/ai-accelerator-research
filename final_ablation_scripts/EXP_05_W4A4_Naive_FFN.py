import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.linalg import hadamard
import math

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def fake_quantize_4bit(tensor, group_size=128):
    """Block-wise symmetric fake quantization to 4-bit (-8 to 7)."""
    orig_shape = tensor.shape
    # Flatten to 2D for grouping if needed, but for simplicity we do per-tensor or per-channel
    # Let's do per-channel (last dimension) min-max to simulate W4/A4
    qmin, qmax = -8, 7
    scale = (tensor.max(dim=-1, keepdim=True)[0] - tensor.min(dim=-1, keepdim=True)[0]) / (qmax - qmin)
    scale = torch.clamp(scale, min=1e-5)
    
    q_tensor = torch.round(tensor / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    return q_tensor * scale

class FakeQuantLinear(nn.Module):
    def __init__(self, original_linear, quantize_w=False, quantize_a=False, smooth_a=False):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.quantize_w = quantize_w
        self.quantize_a = quantize_a
        self.smooth_a = smooth_a
        
        if self.smooth_a:
            # Precompute Hadamard
            dim = self.in_features
            # Need power of 2 for Hadamard. If not, fallback to naive
            if (dim & (dim - 1) == 0) and dim > 0:
                h = torch.tensor(hadamard(dim), dtype=torch.float16, device=self.weight.device) / math.sqrt(dim)
                self.register_buffer("hadamard_matrix", h)
            else:
                self.smooth_a = False

    def forward(self, x):
        w = self.weight
        
        # 1. Quantize Weights
        if self.quantize_w:
            w = fake_quantize_4bit(w)
            
        # 2. Quantize Activations
        if self.quantize_a:
            if self.smooth_a and hasattr(self, "hadamard_matrix"):
                # Smooth outliers before quantization
                x = x @ self.hadamard_matrix
                x = fake_quantize_4bit(x)
                # We also need to transform weights to match the rotated space
                # W' = W @ H^T. For simplicity in this forward pass:
                w = w @ self.hadamard_matrix.T
            else:
                x = fake_quantize_4bit(x)
                
        return F.linear(x, w, self.bias)

def replace_linear_layers(model, quantize_w=False, quantize_a=False, smooth_a=False):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            # Exclude lm_head to prevent total collapse
            if "lm_head" not in name:
                setattr(model, name, FakeQuantLinear(module, quantize_w, quantize_a, smooth_a))
        else:
            replace_linear_layers(module, quantize_w, quantize_a, smooth_a)

def run_ablation():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    questions = [
        "If I have 3 apples and eat 1, how many are left?",
    ]
    
    configs = [
        {"name": "1. Baseline (FP16)", "w": False, "a": False, "smooth": False},
        {"name": "2. W4A16 (Weight-Only 4-bit)", "w": True, "a": False, "smooth": False},
        {"name": "3. W4A4 (Naive 4-bit Activation)", "w": True, "a": True, "smooth": False},
        {"name": "4. W4A4 + Hadamard SmoothAct", "w": True, "a": True, "smooth": True},
    ]
    
    for cfg in configs:
        print(f"\n======================================")
        print(f"Testing Configuration: {cfg['name']}")
        print(f"======================================")
        
        # Reload fresh model for each config to avoid state corruption
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        
        if cfg['w'] or cfg['a']:
            replace_linear_layers(model, quantize_w=cfg['w'], quantize_a=cfg['a'], smooth_a=cfg['smooth'])
            
        for q in questions:
            messages = [{"role": "user", "content": q}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer([text], return_tensors="pt").to(model.device)
            
            start = time.time()
            with torch.no_grad():
                out = model.generate(**inputs, max_new_tokens=20, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            latency = time.time() - start
            
            ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace("\n", " ")
            print(f"Ans: {ans}")
            print(f"Lat: {latency:.2f}s")
            
        # Free memory
        del model
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

if __name__ == "__main__":
    run_ablation()
