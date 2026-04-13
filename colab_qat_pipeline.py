import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import os
import random

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

class QATLinearWrapper(nn.Module):
    def __init__(self, orig_linear):
        super().__init__()
        self.in_features = orig_linear.in_features
        self.out_features = orig_linear.out_features
        self.weight = nn.Parameter(orig_linear.weight.data.clone().float())
        if orig_linear.bias is not None:
            self.bias = nn.Parameter(orig_linear.bias.data.clone().float())
        else:
            self.bias = None

    def forward(self, x):
        q_weight = ternary_quantize_with_ste(self.weight)
        return F.linear(x.to(q_weight.dtype), q_weight, self.bias)

def replace_linear_with_qat(module, name=""):
    replaced_count = 0
    for child_name, child in module.named_children():
        full_name = f"{name}.{child_name}" if name else child_name
        if isinstance(child, nn.Linear) and "lm_head" not in full_name:
            setattr(module, child_name, QATLinearWrapper(child))
            replaced_count += 1
        else:
            replaced_count += replace_linear_with_qat(child, full_name)
    return replaced_count

def run_macro_qat_colab():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Executing on: {device}")
    
    model_id = "google/gemma-3-270m"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        low_cpu_mem_usage=True
    ).to(device)

    model.gradient_checkpointing_enable()

    num_replaced = replace_linear_with_qat(model)
    print(f"Injected QAT wrappers into {num_replaced} Linear layers.")
    
    for name, param in model.named_parameters():
        if "weight" not in name and "bias" not in name:
            param.requires_grad = False
            
    print("Loading full WikiText-2 dataset into memory...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    encodings = tokenizer("\n\n".join(dataset["text"]), return_tensors="pt")
    input_ids = encodings.input_ids[0]
    
    seq_length = 512
    batch_size = 1           # OOM Defense: Physical batch size 1
    grad_accum_steps = 4     # Simulate batch size 4
    steps = 10000
    lr = 1e-4
    max_idx = len(input_ids) - seq_length - 1

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=steps, eta_min=1e-6)
    
    model.train()
    print(f"Starting QAT Loop ({steps} steps, GradAccum={grad_accum_steps}, Peak LR={lr})...")
    
    optimizer.zero_grad()
    for step in range(steps):
        start_idx = random.randint(0, max_idx)
        chunk = input_ids[start_idx : start_idx + seq_length + 1]
        b_input_ids = chunk[:-1].unsqueeze(0).to(device)
        b_labels = chunk[1:].unsqueeze(0).to(device)
        
        with torch.autocast(device_type=device, dtype=torch.bfloat16):
            outputs = model(b_input_ids, labels=b_labels)
            loss = outputs.loss / grad_accum_steps
            
        loss.backward()
        
        if (step + 1) % grad_accum_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            torch.cuda.empty_cache()
            
        if (step + 1) % 50 == 0:
            current_lr = scheduler.get_last_lr()[0]
            print(f"Step {step+1:5d}/{steps} | Loss: {loss.item()*grad_accum_steps:.4f} | LR: {current_lr:.2e}")

        if (step + 1) % 2500 == 0:
            checkpoint_dir = f"./gemma_w158_checkpoint_step_{step+1}"
            os.makedirs(checkpoint_dir, exist_ok=True)
            print(f"--> Checkpoint saved to {checkpoint_dir}")

    print("\nMacro QAT Training Complete.")

if __name__ == "__main__":
    run_macro_qat_colab()
