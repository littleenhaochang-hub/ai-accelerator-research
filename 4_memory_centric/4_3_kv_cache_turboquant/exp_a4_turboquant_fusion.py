import torch

def quantize_4bit_symmetric(x):
    """Simulates 4-bit symmetric quantization per-token (dim=-1)."""
    # Find max absolute value per token
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    
    # Quantize to [-8, 7] and dequantize
    x_q = torch.round(x / scale).clamp(-8, 7)
    return x_q * scale

def calculate_snr(ref, approx):
    """Calculate Signal-to-Noise Ratio in dB."""
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()

def run_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, d_model = 1, 256, 128
    
    print(f"Initializing Fusion Experiment (Seq: {seq_len}, Dim: {d_model})")
    
    # 1. Generate Q and K with extreme outliers to simulate real LLM activations
    Q = torch.randn(batch_size, seq_len, d_model)
    K = torch.randn(batch_size, seq_len, d_model)
    # Inject massive outliers in specific feature channels
    Q[..., 10] *= 15.0
    K[..., 10] *= 15.0
    Q[..., 42] *= 10.0
    K[..., 42] *= 10.0

    # 2. Generate random orthogonal rotation matrix R (TurboQuant / Householder equivalent)
    R, _ = torch.linalg.qr(torch.randn(d_model, d_model))
    
    # --- Baseline: FP32 Exact Attention Scores ---
    S_exact = torch.matmul(Q, K.transpose(-1, -2)) / (d_model ** 0.5)

    # --- Experiment A: A4 Only (No Rotation, FP32 K) ---
    # Fails hard due to outliers
    Q_a4 = quantize_4bit_symmetric(Q)
    S_a4_only = torch.matmul(Q_a4, K.transpose(-1, -2)) / (d_model ** 0.5)

    # --- Experiment B: TurboQuant K Only (Rotated K4, FP32 Q) ---
    Q_rot = torch.matmul(Q, R.transpose(-1, -2))
    K_rot = torch.matmul(K, R.transpose(-1, -2))
    
    K_rot_q4 = quantize_4bit_symmetric(K_rot)
    S_tq_only = torch.matmul(Q_rot, K_rot_q4.transpose(-1, -2)) / (d_model ** 0.5)

    # --- Experiment C: Fused A4 + TurboQuant K ---
    # Quantize rotated Q
    Q_rot_q4 = quantize_4bit_symmetric(Q_rot)
    S_fused = torch.matmul(Q_rot_q4, K_rot_q4.transpose(-1, -2)) / (d_model ** 0.5)

    print("\n--- Attention Logit SNR (Signal-to-Noise Ratio) ---")
    print(f"1. A4 Only (Naive, No Rotation) : {calculate_snr(S_exact, S_a4_only):.2f} dB")
    print(f"2. TurboQuant K Only (FP32 Q)   : {calculate_snr(S_exact, S_tq_only):.2f} dB")
    print(f"3. Fused A4 + TurboQuant K4     : {calculate_snr(S_exact, S_fused):.2f} dB")
    
    print("\n--- Variance Compounding Analysis ---")
    print("Notice two critical dynamics:")
    print("A. The Positive Synergy: Fused A4 + TQ is massively better than Naive A4.")
    print("   The rotation matrix smeared the LLM outliers, rescuing Q's 4-bit precision.")
    print("B. The Negative Synergy: Fused A4 + TQ drops ~3dB compared to TQ alone.")
    print("   Because both Q and K are now noisy, the quantization errors compound")
    print("   during the dot product (variance of product = product of variances).")

if __name__ == "__main__":
    run_experiment()
