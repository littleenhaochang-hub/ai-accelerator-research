import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import warnings
warnings.filterwarnings('ignore')

def quantize_4bit_naive(x):
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def quantize_4bit_percentile(x, p=0.99):
    x_f32 = x.float().abs()
    clip_val = torch.quantile(x_f32, p, dim=-1, keepdim=True)
    clip_val = torch.clamp(clip_val, min=1e-5)
    x_clipped = torch.clamp(x, -clip_val.expand_as(x), clip_val.expand_as(x))
    scale = clip_val / 7.0
    return torch.round(x_clipped / scale).clamp(-8, 7) * scale

def quantize_4bit_group(x, group_size=32):
    shape = x.shape
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    scale = x_g.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_g / scale).clamp(-8, 7) * scale
    return x_q.view(*shape)

def quantize_4bit_sparse_dense(x, threshold_percentile=0.99):
    x_f32 = x.float().abs()
    threshold = torch.quantile(x_f32, threshold_percentile, dim=-1, keepdim=True)
    sparse_mask = x_f32 > threshold
    dense_mask = ~sparse_mask
    
    x_dense = x * dense_mask
    scale = x_dense.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_dense / scale).clamp(-8, 7) * scale
    
    x_sparse = x * sparse_mask
    return x_q + x_sparse

class AttentionQuantizerHook:
    def __init__(self, mode):
        self.mode = mode
        
    def __call__(self, module, input, output):
        if self.mode == "fp16":
            return output
            
        original_dtype = output.dtype
        x = output.float()
        
        if self.mode == "naive":
            return quantize_4bit_naive(x).to(original_dtype)
        elif self.mode == "percentile":
            return quantize_4bit_percentile(x).to(original_dtype)
        elif self.mode == "group":
            return quantize_4bit_group(x).to(original_dtype)
        elif self.mode == "sparse_dense":
            return quantize_4bit_sparse_dense(x).to(original_dtype)

def run_evaluation():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading Qwen2.5-0.5B-Instruct to {device.upper()}...")
    
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
    
    prompts = [
        "What is the capital of France?",
        "Write a python function to compute the Fibonacci sequence.",
        "Translate 'Hello, how are you?' into French.",
        "Summarize the plot of Romeo and Juliet in one sentence.",
        "Why is the sky blue?",
    ]
    
    modes = ["fp16", "naive", "percentile", "group", "sparse_dense"]
    
    print("\nStarting A4A4 Optimization Quality Evaluation Suite...\n")
    
    for i, prompt in enumerate(prompts):
        print(f"\n======================================")
        print(f"Test {i+1}/5: {prompt}")
        print(f"======================================")
        
        inputs = tokenizer(f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n", return_tensors="pt").to(device)
        
        for mode in modes:
            handles = []
            for layer in model.model.layers:
                handles.append(layer.self_attn.q_proj.register_forward_hook(AttentionQuantizerHook(mode)))
                handles.append(layer.self_attn.k_proj.register_forward_hook(AttentionQuantizerHook(mode)))
                handles.append(layer.self_attn.v_proj.register_forward_hook(AttentionQuantizerHook(mode)))
                
            torch.manual_seed(42)
            outputs = model.generate(**inputs, max_new_tokens=25, temperature=0.1, do_sample=True, pad_token_id=tokenizer.eos_token_id)
            text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            text = text.replace('\n', ' ')
            print(f"[{mode.upper():<14}] {text}")
            
            for h in handles:
                h.remove()

if __name__ == "__main__":
    run_evaluation()
