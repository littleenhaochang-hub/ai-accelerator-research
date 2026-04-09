import torch
import torch.nn.functional as F
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

def float_to_fp24(tensor, mode="round"):
    """
    Simulates FP24 (1 sign, 8 exp, 15 mantissa) by truncating/rounding FP32.
    FP32 has 23 mantissa bits, so we mask out the bottom 8 bits.
    """
    t_int = tensor.view(torch.int32)
    if mode == "round":
        # Add half of the dropped precision (2^7) to implement Round-to-Nearest-Even (RNE)
        # Note: Integer addition perfectly handles mantissa overflow into exponent!
        t_int = t_int + 0x00000080
    
    # Mask out the bottom 8 bits
    t_int = t_int & 0xFFFFFF00
    return t_int.view(torch.float32)

def chunked_linear(A, W, chunk_size=32, acc_dtype="fp32", acc_mode="round"):
    """
    Simulates hardware MAC array accumulation.
    A: [B, Seq, K], W: [Out, K]
    We accumulate in blocks of `chunk_size` and truncate the Accumulator register.
    """
    B_dim, Seq, K = A.shape
    Out = W.shape[0]
    
    A_flat = A.view(-1, K)
    acc = torch.zeros((A_flat.shape[0], Out), device=A.device, dtype=torch.float32)
    
    for i in range(0, K, chunk_size):
        A_chunk = A_flat[:, i:i+chunk_size]
        W_chunk = W[:, i:i+chunk_size]
        
        # Partial MAC (multiplier + local adder tree)
        partial = torch.matmul(A_chunk, W_chunk.T)
        
        # Global Accumulator Update
        acc = acc + partial
        
        if acc_dtype == "fp24":
            acc = float_to_fp24(acc, mode=acc_mode)
            
    return acc.view(B_dim, Seq, Out)

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

def run_fp24_experiment():
    print("Initializing FP24 Accumulator Experiment on Qwen2.5-1.5B...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.float32, low_cpu_mem_usage=True).to(device)
    
    # Generate Activation Trace
    text = "Dense compute reduction is critical for AI hardware scaling. " * 10
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        # Extract Layer 12 input
        layer_input = outputs.hidden_states[12].float()
        
    layer = model.model.layers[12]
    
    # We will test the Down Proj (8960 -> 1536) because it has the longest accumulation chain (K=8960)
    # The longer the K, the worse the accumulation noise!
    with torch.no_grad():
        x_norm = layer.post_attention_layernorm(layer_input)
        ffn_intermediate = layer.mlp.act_fn(layer.mlp.gate_proj(x_norm)) * layer.mlp.up_proj(x_norm)
        
        # Real Weights for Down Proj
        W_down = layer.mlp.down_proj.weight.data
        
        # 1. Baseline: Pure FP32 single-shot Matmul
        baseline_out = F.linear(ffn_intermediate, W_down)
        
        experiments = [
            {"name": "FP32 Acc (Chunk 32)", "dtype": "fp32", "mode": "round", "chunk": 32},
            {"name": "FP24 Acc (Chunk 128, Round)", "dtype": "fp24", "mode": "round", "chunk": 128},
            {"name": "FP24 Acc (Chunk 64, Round)", "dtype": "fp24", "mode": "round", "chunk": 64},
            {"name": "FP24 Acc (Chunk 32, Round)", "dtype": "fp24", "mode": "round", "chunk": 32},
            {"name": "FP24 Acc (Chunk 32, Truncate)", "dtype": "fp24", "mode": "trunc", "chunk": 32},
            {"name": "FP24 Acc (Chunk 16, Round)", "dtype": "fp24", "mode": "round", "chunk": 16},
        ]
        
        results = []
        for exp in experiments:
            out = chunked_linear(ffn_intermediate, W_down, chunk_size=exp["chunk"], acc_dtype=exp["dtype"], acc_mode=exp["mode"])
            sqnr = measure_sqnr(baseline_out, out)
            results.append({
                "Architecture": exp["name"],
                "Accumulations (K/chunk)": W_down.shape[1] // exp["chunk"],
                "SQNR (dB)": round(sqnr, 2)
            })
            
        df = pd.DataFrame(results)
        print("\n" + df.to_markdown(index=False))

if __name__ == "__main__":
    run_fp24_experiment()
