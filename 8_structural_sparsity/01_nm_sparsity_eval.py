import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def apply_2_4_sparsity(tensor):
    """
    Simulates N:M (2:4) structural sparsity.
    For every block of 4 elements, keeps the 2 with the highest magnitude and zeros the rest.
    """
    orig_shape = tensor.shape
    # Flatten out the inner dimension into blocks of 4
    if tensor.shape[-1] % 4 != 0:
        return tensor # Skip if not divisible
    
    tensor_blocked = tensor.view(-1, 4)
    
    # Get the indices of the top 2 elements by absolute magnitude
    _, indices = torch.topk(torch.abs(tensor_blocked), 2, dim=-1)
    
    # Create a mask
    mask = torch.zeros_like(tensor_blocked, dtype=torch.bool)
    mask.scatter_(-1, indices, True)
    
    # Apply mask
    sparse_tensor = tensor_blocked * mask
    return sparse_tensor.view(orig_shape)

class SparseLinear(nn.Module):
    def __init__(self, original_linear, sparsity_type="2:4_weight"):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias
        self.sparsity_type = sparsity_type

    def forward(self, x):
        w = self.weight
        if "weight" in self.sparsity_type:
            w = apply_2_4_sparsity(w)
            
        if "activation" in self.sparsity_type:
            x = apply_2_4_sparsity(x)
            
        return F.linear(x, w, self.bias)

def apply_sparsity_patch(model, sparsity_type="2:4_weight"):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            if "lm_head" not in name:
                setattr(model, name, SparseLinear(module, sparsity_type))
        else:
            apply_sparsity_patch(module, sparsity_type)

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
        {"name": "1. 2:4 Weight Sparsity (50% MAC reduction)", "type": "2:4_weight"},
        {"name": "2. 2:4 Activation Sparsity (Dynamic Routing)", "type": "2:4_activation"},
        {"name": "3. 2:4 Dual Sparsity (Weights + Activations)", "type": "2:4_weight_activation"}
    ]
    
    for cfg in configs:
        print(f"\n======================================")
        print(f"Testing: {cfg['name']}")
        print(f"======================================")
        
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        apply_sparsity_patch(model, cfg["type"])

        with torch.no_grad():
            out = model.generate(**inputs.to(model.device), max_new_tokens=15, pad_token_id=tokenizer.eos_token_id, do_sample=False)
            quant_hidden = model(inputs.input_ids.to(model.device), output_hidden_states=True).hidden_states[-1]
            
        ans = tokenizer.decode(out[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True).strip().replace('\n', ' ')
        print(f"Output: {ans}")
        
        cos_sim = F.cosine_similarity(base_hidden, quant_hidden, dim=-1).mean().item()
        snr = 10 * torch.log10(torch.mean(base_hidden**2) / torch.mean((base_hidden - quant_hidden)**2)).item()
        print(f"Metrics -> Cosine Sim: {cos_sim:.4f} | SNR: {snr:.2f} dB")
        
        del model
        torch.cuda.empty_cache()

if __name__ == "__main__":
    run()
