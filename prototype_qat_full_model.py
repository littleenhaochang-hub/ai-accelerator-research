import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import os
from tqdm import tqdm
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
        return F.linear(x.float(), q_weight, self.bias).to(x.dtype)

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

def run_full_qat():
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

    print(f"Loading {model_id} for Full-Model QAT...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        low_cpu_mem_usage=True, 
        token=token, 
        cache_dir=cache_dir
    ).to(device)

    # Replace Linear layers with QAT wrappers
    num_replaced = replace_linear_with_qat(model)
    print(f"Injected QAT wrappers into {num_replaced} Linear layers.")
    
    # Freeze everything except the QAT Linear weights (and embeddings/layernorms if we wanted, but let's just train the QAT weights)
    for name, param in model.named_parameters():
        if "weight" not in name and "bias" not in name:
            param.requires_grad = False
            
    print("Loading tiny WikiText-2 subset for QAT micro-training...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:5%]")
    encodings = tokenizer("\n\n".join(dataset["text"]), return_tensors="pt")
    
    # Hyperparameters
    seq_length = 512
    batch_size = 2
    steps = 150 # Quick micro-training loop
    lr = 5e-5
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    model.train()
    
    print(f"Starting QAT Loop ({steps} steps, seq_len={seq_length}, batch_size={batch_size}, lr={lr})...")
    
    input_ids = encodings.input_ids[0]
    max_idx = len(input_ids) - seq_length - 1
    
    import random
    
    for step in range(steps):
        batch_inputs = []
        batch_labels = []
        for _ in range(batch_size):
            start_idx = random.randint(0, max_idx)
            chunk = input_ids[start_idx : start_idx + seq_length + 1]
            batch_inputs.append(chunk[:-1])
            batch_labels.append(chunk[1:])
            
        b_input_ids = torch.stack(batch_inputs).to(device)
        b_labels = torch.stack(batch_labels).to(device)
        
        optimizer.zero_grad()
        outputs = model(b_input_ids, labels=b_labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        
        if (step + 1) % 10 == 0:
            print(f"Step {step+1:3d}/{steps} | CrossEntropyLoss: {loss.item():.4f}")

    print("\nQAT Training Complete. Transitioning to PPL Evaluation on Test Split...")
    model.eval()
    qat_ppl = evaluate_ppl(model, tokenizer, sequence_length=1024)
    print(f"\n[QAT Verdict] Full-Model W1.58 PPL (After {steps} steps): {qat_ppl:.4f}")

if __name__ == "__main__":
    run_full_qat()