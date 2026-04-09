import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

NF4_LUT = torch.tensor([-1.0, -0.6961928, -0.5250731, -0.3949175, -0.2844414, -0.1847734, -0.0910500, 0.0, 0.0795803, 0.1609302, 0.2461123, 0.3379152, 0.4407098, 0.5626170, 0.7229568, 1.0])

def e8m0_scale(amax): return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

def fake_quant_subchannel(x, bits=8, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0: x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True)
    scale = e8m0_scale(amax / ((2**(bits-1)) - 1))
    q = torch.round(x_blocked / scale)
    q = torch.clamp(q, -(2**(bits-1)), (2**(bits-1)) - 1)
    dq = q * scale
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0: dq = dq[..., :-pad_len]
    return dq

def fake_quant_nf4_lut(x, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0: x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True).clamp(min=1e-7)
    x_scaled = x_blocked / amax
    lut = NF4_LUT.to(device=x.device, dtype=x.dtype)
    diffs = torch.abs(x_scaled.unsqueeze(-1) - lut)
    indices = torch.argmin(diffs, dim=-1)
    q = lut[indices]
    dq = q * amax
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0: dq = dq[..., :-pad_len]
    return dq

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

# We only focus on the Matrix Multiplication A8 * W4 here to isolate the LUT utility
def simulate_a8w4_linear(A, W, block_size=128):
    # A is A8 (8-bit subchannel)
    A_q = fake_quant_subchannel(A, bits=8, block_size=block_size)
    # W is W4 (4-bit linear subchannel)
    W_q = fake_quant_subchannel(W, bits=4, block_size=block_size)
    return torch.matmul(A_q, W_q.T)

def simulate_a8w4_lut(A, W, block_size=128):
    # A is A8 (8-bit subchannel)
    A_q = fake_quant_subchannel(A, bits=8, block_size=block_size)
    # W is W4 (4-bit NF4 LUT)
    W_q = fake_quant_nf4_lut(W, block_size=block_size)
    return torch.matmul(A_q, W_q.T)

def run_a8w4_ablation():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print("Initializing A8W4 Mathematical Trace...")
    
    # 1. Hardware Matrix Dimension Setup (Simulating a standard FFN linear layer)
    B, Seq, In_Dim, Out_Dim = 1, 1024, 1536, 4096
    
    # 2. Generate Real-world Heavy-Tail Activations (A) and Normal Weights (W)
    torch.manual_seed(42)
    dist_a = torch.distributions.studentT.StudentT(df=3.0)
    A = dist_a.rsample((B, Seq, In_Dim)).to(torch.bfloat16).to(device)
    
    W = torch.randn(Out_Dim, In_Dim).to(torch.bfloat16).to(device)
    # Normalize W to simulate layer init
    W = W / math.sqrt(In_Dim) if 'math' in globals() else W / (In_Dim**0.5)

    # Baseline BF16 * BF16
    baseline_out = torch.matmul(A, W.T)
    
    # Trace 1: Linear A4W4 (For reference)
    linear_a4w4_out = torch.matmul(fake_quant_subchannel(A, bits=4), fake_quant_subchannel(W, bits=4).T)
    sqnr_a4w4_linear = measure_sqnr(baseline_out, linear_a4w4_out)
    
    # Trace 2: Linear A8W4
    linear_a8w4_out = simulate_a8w4_linear(A, W)
    sqnr_linear = measure_sqnr(baseline_out, linear_a8w4_out)
    
    # Trace 3: LUT A8W4
    lut_a8w4_out = simulate_a8w4_lut(A, W)
    sqnr_lut = measure_sqnr(baseline_out, lut_a8w4_out)
    
    print("\n| Configuration | SQNR (dB) | Memory (W/A) |")
    print("| :--- | :--- | :--- |")
    print(f"| A4W4 (Linear) | {sqnr_a4w4_linear:.2f} | 0.25x / 0.25x |")
    print(f"| A8W4 (Linear) | {sqnr_linear:.2f} | 0.25x / 0.50x |")
    print(f"| A8W4 (NF4 LUT) | {sqnr_lut:.2f} | 0.25x / 0.50x |")

if __name__ == "__main__":
    run_a8w4_ablation()
