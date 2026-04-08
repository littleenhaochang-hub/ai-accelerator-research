import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# --- Quantization Core (From Ablation) ---

def e8m0_scale(amax):
    return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

def fake_quant_subchannel(x, bits=8, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0:
        x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True)
    scale = e8m0_scale(amax / ((2**(bits-1)) - 1))
    q = torch.round(x_blocked / scale)
    q = torch.clamp(q, -(2**(bits-1)), (2**(bits-1)) - 1)
    dq = q * scale
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0:
        dq = dq[..., :-pad_len]
    return dq

def simulate_chained_householder(x, num_reflections=4):
    orig_shape = x.shape
    if len(orig_shape) == 3:
        B, Seq, H = orig_shape
        x_reshaped = x.view(-1, H)
    else:
        H = orig_shape[-1]
        x_reshaped = x.view(-1, H)
    torch.manual_seed(42)
    for _ in range(num_reflections):
        v = torch.randn(H, device=x.device, dtype=x.dtype)
        v = v / torch.norm(v)
        proj = torch.matmul(x_reshaped, v.unsqueeze(1))
        x_reshaped = x_reshaped - 2 * proj * v.unsqueeze(0)
    return x_reshaped.view(orig_shape)

def fake_quant_turboquant(x, bits=4, block_size=128):
    smeared = simulate_chained_householder(x)
    fq = fake_quant_subchannel(smeared, bits=bits, block_size=block_size)
    restored = simulate_chained_householder(fq)
    return restored

# --- Module Wrappers for Dynamic Injection ---

class QuantizedMLP(torch.nn.Module):
    def __init__(self, orig_mlp, bits=4):
        super().__init__()
        self.orig_mlp = orig_mlp
        self.bits = bits
        
    def forward(self, x):
        x_q = fake_quant_subchannel(x, bits=self.bits)
        out = self.orig_mlp(x_q)
        out_q = fake_quant_subchannel(out, bits=self.bits)
        return out_q

class QuantizedAttn(torch.nn.Module):
    def __init__(self, orig_attn, bits=4):
        super().__init__()
        self.orig_attn = orig_attn
        self.bits = bits
        
    def forward(self, hidden_states, *args, **kwargs):
        x_q = fake_quant_turboquant(hidden_states, bits=self.bits)
        out = self.orig_attn(x_q, *args, **kwargs)
        attn_out_q = fake_quant_subchannel(out[0], bits=self.bits)
        return (attn_out_q,) + out[1:]

def inject_quantization(model, config="tape-out"):
    print(f"Injecting {config} quantization scheme into all layers...")
    for layer in model.model.layers:
        if config == "tape-out":
            # Tape-out: A4KV4 Turbo + A4W4 Subchannel
            layer.mlp = QuantizedMLP(layer.mlp, bits=4)
            layer.self_attn = QuantizedAttn(layer.self_attn, bits=4)

# --- Perplexity Evaluation ---

def evaluate_ppl(model, tokenizer, dataset, seq_len=1024, num_samples=20):
    text = "\n\n".join(dataset["text"][:1000]) # Take a large enough chunk
    encodings = tokenizer(text, return_tensors="pt")
    
    nlls = []
    total_len = encodings.input_ids.size(1)
    samples_to_run = min(num_samples, total_len // seq_len)
    
    for i in tqdm(range(samples_to_run), desc="Evaluating PPL"):
        begin_loc = i * seq_len
        end_loc = begin_loc + seq_len
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(model.device)
        target_ids = input_ids.clone()
        
        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            nlls.append(outputs.loss)
            
    ppl = torch.exp(torch.stack(nlls).mean()).item()
    return ppl

def main():
    model_id = "Qwen/Qwen2.5-1.5B"
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    print("Loading Model and Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    
    print("Loading WikiText-2 Dataset...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
    
    # 1. Evaluate Baseline BF16
    print("\n--- Running Baseline (BF16) ---")
    ppl_baseline = evaluate_ppl(model, tokenizer, dataset)
    print(f"-> Baseline PPL: {ppl_baseline:.3f}")
    
    # 2. Inject FakeQuant & Evaluate Tape-out
    print("\n--- Running Tape-out Architecture (A4W4 + A4KV4) ---")
    inject_quantization(model, config="tape-out")
    ppl_tapeout = evaluate_ppl(model, tokenizer, dataset)
    print(f"-> Tape-out PPL: {ppl_tapeout:.3f}")
    
    # Summary
    print("\n==========================================================")
    print("FINAL PERPLEXITY PROJECTION (WikiText-2, seq_len=1024)")
    print("==========================================================")
    print(f"Baseline (BF16) PPL    : {ppl_baseline:.3f}")
    print(f"Tape-out (A4-bit) PPL  : {ppl_tapeout:.3f}")
    delta = ((ppl_tapeout - ppl_baseline) / ppl_baseline) * 100
    print(f"Degradation            : +{delta:.2f}%")
    print("==========================================================")

if __name__ == "__main__":
    main()
