import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import warnings
warnings.filterwarnings('ignore')

def quantize_4bit_symmetric(x):
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def get_rot_matrix(dim, device):
    torch.manual_seed(42)
    R, _ = torch.linalg.qr(torch.randn(dim, dim, device="cpu"))
    return R.to(device)

class AttentionQuantizerHook:
    def __init__(self, mode, R, is_q=False):
        self.mode = mode
        self.R = R
        self.is_q = is_q
        
    def __call__(self, module, input, output):
        if self.mode == "fp16":
            return output
            
        original_dtype = output.dtype
        x = output.float()
        
        # If the mode specifies FP16 activations, skip quantizing Q entirely.
        if "fp16_act" in self.mode and self.is_q:
            return output

        if self.mode.startswith("naive_a4"):
            out = quantize_4bit_symmetric(x)
            return out.to(original_dtype)
            
        elif self.mode.startswith("turboquant") and "qjl" not in self.mode:
            rotated = torch.matmul(x, self.R)
            q4 = quantize_4bit_symmetric(rotated)
            out = torch.matmul(q4, self.R.T)
            return out.to(original_dtype)
            
        elif "turboquant" in self.mode and "qjl" in self.mode:
            rotated = torch.matmul(x, self.R)
            q4 = quantize_4bit_symmetric(rotated)
            
            err = rotated - q4
            sign_1bit = torch.sign(err)
            sign_1bit[sign_1bit == 0] = 1.0
            scale = err.abs().mean(dim=-1, keepdim=True)
            res_1bit = sign_1bit * scale
            
            recovered = q4 + res_1bit
            out = torch.matmul(recovered, self.R.T)
            return out.to(original_dtype)

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
        "What is 15 multiplied by 4?",
        "Name three primary colors.",
        "Write a short haiku about a robot.",
        "Explain quantum computing to a 5-year-old in one sentence.",
        "List two benefits of regular exercise."
    ]
    
    q_dim = model.config.hidden_size
    kv_dim = model.config.hidden_size // (model.config.num_attention_heads // model.config.num_key_value_heads)
    
    R_q = get_rot_matrix(q_dim, device)
    R_kv = get_rot_matrix(kv_dim, device)
    
    modes = ["fp16", "turboquant_fp16_act", "turboquant_fp16_act_qjl"]
    
    print("\nStarting KV-Only Quality Evaluation Suite...\n")
    
    for i, prompt in enumerate(prompts[:5]): # Run 5 tests for speed
        print(f"\n======================================")
        print(f"Test {i+1}/5: {prompt}")
        print(f"======================================")
        
        inputs = tokenizer(f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n", return_tensors="pt").to(device)
        
        for mode in modes:
            handles = []
            for layer in model.model.layers:
                handles.append(layer.self_attn.q_proj.register_forward_hook(AttentionQuantizerHook(mode, R_q, is_q=True)))
                handles.append(layer.self_attn.k_proj.register_forward_hook(AttentionQuantizerHook(mode, R_kv, is_q=False)))
                handles.append(layer.self_attn.v_proj.register_forward_hook(AttentionQuantizerHook(mode, R_kv, is_q=False)))
                
            torch.manual_seed(42)
            outputs = model.generate(**inputs, max_new_tokens=25, temperature=0.1, do_sample=True, pad_token_id=tokenizer.eos_token_id)
            text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            
            # Format text to replace newlines with spaces for clean printing
            text = text.replace('\n', ' ')
            print(f"[{mode.upper():<14}] {text}")
            
            for h in handles:
                h.remove()

if __name__ == "__main__":
    run_evaluation()
