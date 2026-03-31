import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
warnings.filterwarnings('ignore')

def quantize_4bit_naive(x):
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def quantize_4bit_subchannel_fp16(x, group_size=32):
    shape = x.shape
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    scale = x_g.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_g / scale).clamp(-8, 7) * scale
    return x_q.view(*shape)

def quantize_4bit_subchannel_e8m0(x, group_size=32):
    shape = x.shape
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    max_val = x_g.abs().max(dim=-1, keepdim=True).values
    max_val = torch.clamp(max_val, min=1e-5)
    ideal_scale = max_val / 7.0
    exponent = torch.ceil(torch.log2(ideal_scale))
    scale_e8m0 = torch.pow(2.0, exponent)
    x_q = torch.round(x_g / scale_e8m0).clamp(-8, 7) * scale_e8m0
    return x_q.view(*shape)

def get_rot_matrix(dim, device):
    torch.manual_seed(42)
    R, _ = torch.linalg.qr(torch.randn(dim, dim, device="cpu"))
    return R.to(device)

class AblationHook:
    def __init__(self, mode, stage, R, is_q=False):
        self.mode = mode
        self.stage = stage
        self.R = R
        self.is_q = is_q
        
    def __call__(self, module, input, output):
        if self.mode == "fp16":
            return output
            
        # STAGE 1: KV4 Only. If this is Q, skip quantization.
        if self.stage == 1 and self.is_q:
            return output

        original_dtype = output.dtype
        x = output.float()
        
        if self.mode == "naive":
            return quantize_4bit_naive(x).to(original_dtype)
            
        elif self.mode == "sub_fp16":
            return quantize_4bit_subchannel_fp16(x).to(original_dtype)
            
        elif self.mode == "sub_e8m0":
            return quantize_4bit_subchannel_e8m0(x).to(original_dtype)
            
        elif self.mode == "turboquant":
            rotated = torch.matmul(x, self.R)
            q4 = quantize_4bit_naive(rotated)
            return torch.matmul(q4, self.R.T).to(original_dtype)
            
        elif self.mode == "turboquant_qjl":
            rotated = torch.matmul(x, self.R)
            q4 = quantize_4bit_naive(rotated)
            
            err = rotated - q4
            sign_1bit = torch.sign(err)
            sign_1bit[sign_1bit == 0] = 1.0
            scale = err.abs().mean(dim=-1, keepdim=True)
            res_1bit = sign_1bit * scale
            
            recovered = q4 + res_1bit
            return torch.matmul(recovered, self.R.T).to(original_dtype)

def run_qwen_ablation():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading Qwen2.5-0.5B-Instruct to {device.upper()}...")
    
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
    
    prompts = [
        "What is the capital of France?",
        "Write a python function to compute the Fibonacci sequence.",
        "Why is the sky blue?"
    ]
    
    q_dim = model.config.hidden_size
    kv_dim = model.config.hidden_size // (model.config.num_attention_heads // model.config.num_key_value_heads)
    R_q = get_rot_matrix(q_dim, device)
    R_kv = get_rot_matrix(kv_dim, device)
    
    modes = ["fp16", "naive", "sub_fp16", "sub_e8m0", "turboquant", "turboquant_qjl"]
    stages = [1, 2] # 1 = KV4, 2 = A4KV4
    
    print("\nStarting Qwen Generation Ablation (Gate B)...\n")
    
    for stage in stages:
        stage_name = "STAGE 1: KV4 (Q is FP32)" if stage == 1 else "STAGE 2: A4 KV4 (Q is 4-bit)"
        print(f"\n{'='*60}")
        print(f" {stage_name}")
        print(f"{'='*60}")
        
        for i, prompt in enumerate(prompts):
            print(f"\n--- Prompt {i+1}: {prompt} ---")
            inputs = tokenizer(f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n", return_tensors="pt").to(device)
            
            for mode in modes:
                handles = []
                for layer in model.model.layers:
                    handles.append(layer.self_attn.q_proj.register_forward_hook(AblationHook(mode, stage, R_q, is_q=True)))
                    handles.append(layer.self_attn.k_proj.register_forward_hook(AblationHook(mode, stage, R_kv, is_q=False)))
                    handles.append(layer.self_attn.v_proj.register_forward_hook(AblationHook(mode, stage, R_kv, is_q=False)))
                    
                torch.manual_seed(42)
                outputs = model.generate(**inputs, max_new_tokens=20, temperature=0.1, do_sample=True, pad_token_id=tokenizer.eos_token_id)
                text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
                text = text.replace('\n', ' ')
                
                print(f"[{mode.upper():<14}] {text}")
                
                for h in handles:
                    h.remove()

if __name__ == "__main__":
    run_qwen_ablation()
