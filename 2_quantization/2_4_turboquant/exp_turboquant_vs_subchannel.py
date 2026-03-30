import torch

def quantize_4bit_tokenwise(x):
    """Standard token-wise 4-bit symmetric quantization (1 scale per token)."""
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def quantize_4bit_subchannel(x, group_size=32):
    """Sub-channel (Group/Block) 4-bit quantization (1 scale per block)."""
    shape = x.shape
    # Reshape to isolate groups: [batch, seq, num_groups, group_size]
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    
    # Scale factor PER GROUP
    scale = x_g.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    
    x_q = torch.round(x_g / scale).clamp(-8, 7) * scale
    return x_q.view(*shape)

def get_rot_matrix(dim):
    torch.manual_seed(42)
    R, _ = torch.linalg.qr(torch.randn(dim, dim))
    return R

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    return (10 * torch.log10(signal_power / noise_power)).item()

def run_comparison():
    torch.manual_seed(42)
    batch, seq, d_model = 1, 256, 4096
    group_size = 32
    
    print(f"Comparing TurboQuant vs Sub-Channel Quantization")
    print(f"Vector Dim: {d_model} | Sub-channel Group Size: {group_size}")
    
    # 1. Generate LLM Activations with Outliers
    X = torch.randn(batch, seq, d_model)
    # Inject massive outliers to simulate real LLM behavior
    X[..., 15] *= 25.0
    X[..., 1024] *= 20.0
    X[..., 2048] *= 30.0
    
    # --- Baseline: Naive 4-Bit Token-wise ---
    X_naive = quantize_4bit_tokenwise(X)
    snr_naive = calculate_snr(X, X_naive)
    
    # --- Method A: Sub-Channel Quantization ---
    X_subchannel = quantize_4bit_subchannel(X, group_size)
    snr_subchannel = calculate_snr(X, X_subchannel)
    
    # --- Method B: TurboQuant (Orthogonal Rotation + Token-wise 4-Bit) ---
    R = get_rot_matrix(d_model)
    X_rotated = torch.matmul(X, R)
    X_rotated_q = quantize_4bit_tokenwise(X_rotated)
    X_turboquant = torch.matmul(X_rotated_q, R.T) # Un-rotate
    snr_turboquant = calculate_snr(X, X_turboquant)
    
    print("\n--- Reconstruction SNR (Higher dB is better) ---")
    print(f"1. Naive 4-Bit (1 scale/token)     : {snr_naive:>6.2f} dB  <- Outliers destroyed it")
    print(f"2. Sub-Channel Quant (128 scales)  : {snr_subchannel:>6.2f} dB  <- Outliers isolated")
    print(f"3. TurboQuant (1 scale + Rotation) : {snr_turboquant:>6.2f} dB  <- Outliers smeared")
    
    print("\n--- Hardware Tradeoffs Analysis ---")
    
    # Calculate scale factor memory
    scales_naive = seq * 1 * 2  # 1 FP16 scale per token
    scales_sub = seq * (d_model // group_size) * 2  # 128 FP16 scales per token
    
    print("[Memory Overhead for Scales (per sequence)]")
    print(f"TurboQuant / Naive : {scales_naive} Bytes")
    print(f"Sub-Channel Quant  : {scales_sub} Bytes ({scales_sub / scales_naive:.1f}x more memory for scales)")
    
    print("\n[Compute Overhead]")
    print("TurboQuant        : Requires an O(N^2) dense matrix multiplication (X @ R) before quantization.")
    print("Sub-Channel Quant : ZERO extra compute. Just reshapes and local max() calls.")

if __name__ == "__main__":
    run_comparison()
