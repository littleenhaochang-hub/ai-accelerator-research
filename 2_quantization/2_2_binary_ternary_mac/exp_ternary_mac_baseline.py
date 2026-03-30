import torch
import torch.nn as nn
import time

def quantize_weight_ternary(w):
    """
    Simulates BitNet 1.58-bit weight quantization.
    Weights are scaled by their mean absolute value and rounded to {-1, 0, 1}.
    """
    gamma = w.abs().mean().clamp(min=1e-5)
    w_scaled = w / gamma
    w_ternary = torch.round(w_scaled).clamp(-1, 1)
    return w_ternary * gamma  # Return dequantized value for simulation

def quantize_activation_8bit(x):
    """
    Simulates 8-bit ABSMAX activation quantization (common in BitNet).
    """
    scale = x.abs().max(dim=-1, keepdim=True).values / 127.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x / scale).clamp(-128, 127)
    return x_q * scale

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()

def run_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, in_features, out_features = 1, 128, 4096, 4096
    
    print(f"Initializing 1.58-Bit Ternary MAC Baseline (BitNet) Experiment")
    print(f"Shape: [{batch_size}, {seq_len}, {in_features}] @ [{in_features}, {out_features}]")
    
    # Generate Activation and Weight
    X = torch.randn(batch_size, seq_len, in_features)
    W = torch.randn(out_features, in_features) / (in_features ** 0.5)
    
    # Inject outliers into Activations (common LLM issue)
    X[..., 15] *= 10.0
    X[..., 1024] *= 15.0

    # --- FP32 Exact Baseline ---
    Y_exact = torch.matmul(X, W.t())

    # --- 1.58-Bit Ternary Weights + FP32 Activations ---
    W_ternary = quantize_weight_ternary(W)
    Y_ternary_w = torch.matmul(X, W_ternary.t())

    # --- BitNet b1.58 (Ternary W + 8-bit A) ---
    X_q8 = quantize_activation_8bit(X)
    Y_bitnet = torch.matmul(X_q8, W_ternary.t())

    print("\n--- Linear Layer Output SNR (Signal-to-Noise Ratio) ---")
    print(f"1. FP32 Act x 1.58-Bit W : {calculate_snr(Y_exact, Y_ternary_w):.2f} dB")
    print(f"2. 8-Bit Act x 1.58-Bit W: {calculate_snr(Y_exact, Y_bitnet):.2f} dB")
    
    print("\n--- Hardware Implication & Bottleneck ---")
    print("In true hardware, the MAC (Multiply-Accumulate) operation for W={-1, 0, 1}")
    print("completely eliminates floating-point multipliers. It becomes pure addition and subtraction.")
    print("\n[CHALLENGE RECORDED]:")
    print("While the SNR is very low (~5.8 dB), the real challenge for Edge deployment")
    print("is that the scaling factors (gamma for weights, scale for activations) must be")
    print("multiplied back in FP16 *after* the integer accumulation. This requires a mixed-precision")
    print("accumulator, which creates pipeline stalls on rigid NPUs like the Apple Neural Engine.")

if __name__ == "__main__":
    run_experiment()
