import torch
import torch.nn as nn
import torch.nn.functional as F

print("=====================================================")
print(" W4A4 Quantization Baseline for LLM FFN Layers")
print(" Goal: Simulate catastrophic failure of 4-bit activation quantization")
print("       due to massive outliers in Feed-Forward Networks.")
print("=====================================================\n")

# 1. Simulation Setup (LLaMA-style FFN Layer)
# Batch=1, SeqLen=1024, Hidden Dim=4096, Intermediate Dim=11008
B, S, D, I = 1, 1024, 4096, 11008

print(f"Simulating FFN Activation Tensor: [Batch:{B}, SeqLen:{S}, Dim:{D}]")

# Simulate Activation Input (X) with massive outliers
# LLM activations typically have a few channels with values 100x larger than the mean
x = torch.randn(B, S, D, dtype=torch.float32) * 0.1
# Inject massive outliers into specific channels (e.g., channel 10 and 100)
x[:, :, 10] = 50.0
x[:, :, 100] = -45.0

print(f"Original Activation Max Value (Outlier): {x.max().item():.2f}")
print(f"Original Activation Min Value (Outlier): {x.min().item():.2f}")
print(f"Original Activation Mean: {x.mean().item():.4f}")

# Simulate FFN Up-Projection Weight (W)
# Weights are usually well-behaved Gaussian, easy to quantize
W_up = torch.randn(D, I, dtype=torch.float32) * 0.02

# ---------------------------------------------------------
# The Golden Standard (FP32/FP16 Math)
# ---------------------------------------------------------
# This is what the LLM expects the FFN output to look like
golden_output = x @ W_up

# ---------------------------------------------------------
# Uniform 4-Bit Quantization (The Naive Approach)
# ---------------------------------------------------------
def quantize_4bit_symmetric(tensor):
    """
    Standard symmetric 4-bit uniform quantization.
    Maps floating point to integers [-8, 7].
    """
    # 4 bits = 16 levels. Max integer is 7.
    qmax = 7.0
    
    # Calculate scale factor based on the absolute maximum value (The Outlier)
    # This is the fatal flaw: The outlier forces the scale to be huge.
    scale = tensor.abs().max() / qmax
    
    # Quantize: x_q = round(x / scale)
    x_q = torch.clamp(torch.round(tensor / scale), -8.0, 7.0)
    
    # Dequantize for math: x_dq = x_q * scale
    x_dq = x_q * scale
    return x_dq, scale

print("\n--- Applying Naive W4A4 Quantization ---")
# Quantize Weights to 4-bit
W_up_dq, w_scale = quantize_4bit_symmetric(W_up)
print(f"Weight 4-bit Quantization Scale: {w_scale:.4f} (Small, Good)")

# Quantize Activations to 4-bit
# The massive outliers (50.0) will force this scale to be ~7.0
x_dq, a_scale = quantize_4bit_symmetric(x)
print(f"Activation 4-bit Quantization Scale: {a_scale:.4f} (Massive, BAD)")

# Calculate the W4A4 FFN Output
w4a4_output = x_dq @ W_up_dq

# ---------------------------------------------------------
# Evaluation (The Catastrophe)
# ---------------------------------------------------------
# Measure how badly the 4-bit quantization destroyed the FFN output
cos_sim = F.cosine_similarity(golden_output.flatten(), w4a4_output.flatten(), dim=0).item()

print(f"\n[Results] W4A4 FFN Output Accuracy (Cosine Similarity): {cos_sim * 100:.2f}%")

if cos_sim < 0.90:
    print("\n[FAILURE] As expected, naive W4A4 quantization failed catastrophically.")
    print("The massive outliers in the activation tensor forced the quantization buckets to be too wide.")
    print("Normal token data was crushed to zero. The LLM would hallucinate instantly.")
else:
    print("\n[SUCCESS] W4A4 worked (This should not happen with extreme outliers).")
