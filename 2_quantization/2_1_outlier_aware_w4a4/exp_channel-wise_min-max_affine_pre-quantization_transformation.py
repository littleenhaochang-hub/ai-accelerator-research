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
# Inject another outlier for diversity
x[:, :, 200] = 75.0
# Inject a constant channel (to test flat_mask logic)
x[:, :, 300] = 2.5 # All values in this channel are 2.5
x[:, :, 301] = 0.0 # All values in this channel are 0.0

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
    
    # Calculate scale factor based on the absolute maximum value
    scale = tensor.abs().max() / qmax
    
    # Handle case where tensor is all zeros (abs().max() is 0)
    if scale == 0:
        scale = 1.0 # Prevent division by zero; dequant will be all zeros.
    
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
x_dq_naive, a_scale_naive = quantize_4bit_symmetric(x)
print(f"Activation 4-bit Quantization Scale (Naive): {a_scale_naive:.4f} (Massive, BAD)")

# Calculate the W4A4 FFN Output
w4a4_output_naive = x_dq_naive @ W_up_dq

# ---------------------------------------------------------
# Novel: Channel-wise Min-Max Affine Pre-Quantization Transformation
# ---------------------------------------------------------
def channel_wise_affine_quantize_4bit_symmetric(tensor):
    """
    Applies channel-wise min-max affine transformation, then global 4-bit symmetric quantization,
    and finally inverse affine transformation.
    """
    # 4 bits = 16 levels. Max integer is 7.
    qmax = 7.0

    original_shape = tensor.shape
    # Flatten B*S into one dimension for channel min/max computation: (B, S, D) -> (B*S, D)
    x_flat_bs_d = tensor.view(-1, original_shape[-1]) 

    # Compute min/max for each channel (dimension D)
    # min_vals, max_vals will be of shape (D,)
    min_vals = x_flat_bs_d.min(dim=0).values
    max_vals = x_flat_bs_d.max(dim=0).values

    # Initialize scaling factors (s_c) and shifting biases (z_c)
    s_c = torch.zeros_like(min_vals)
    z_c = torch.zeros_like(min_vals)

    # Calculate s_c and z_c for each channel such that min_xc maps to -qmax and max_xc maps to qmax
    # s_c * min_xc + z_c = -qmax
    # s_c * max_xc + z_c = qmax
    # => s_c = (2 * qmax) / (max_xc - min_xc)
    # => z_c = qmax - s_c * max_xc

    # Handle cases where max_xc == min_xc (constant channel)
    diff = max_vals - min_vals
    
    # Use a small epsilon to avoid numerical issues when channels are near constant
    non_flat_mask = diff > 1e-6 
    
    s_c[non_flat_mask] = (2 * qmax) / diff[non_flat_mask]
    z_c[non_flat_mask] = qmax - s_c[non_flat_mask] * max_vals[non_flat_mask]

    # For flat channels (diff is very small or zero):
    # If a channel is constant positive, map to qmax. If constant negative, to -qmax. If zero, to 0.
    # This ensures the transformed channel's abs().max() is qmax (or 0 if original was 0)
    flat_mask = ~non_flat_mask
    z_c[flat_mask] = torch.where(min_vals[flat_mask] > 0, qmax,
                                 torch.where(min_vals[flat_mask] < 0, -qmax, 0.0))
    # s_c remains 0 for flat channels, as it's a constant value.

    # Apply affine transformation: y = s_c * x + z_c
    # s_c and z_c are (D,) and will broadcast correctly to (B, S, D)
    y = s_c * tensor + z_c
    
    # Perform global 4-bit symmetric quantization on the transformed tensor y
    # This inner function should now ideally produce a scale close to 1.0
    # because each channel's range in 'y' is mapped to [-qmax, qmax] (or 0).
    y_dq, global_a_scale_novel = quantize_4bit_symmetric(y) # Re-using the standard quantizer

    # Apply inverse affine transformation: x_dq = (y_dq - z_c) / s_c
    x_dq_novel = torch.zeros_like(tensor)
    
    # Inverse for non-flat channels
    # The non_flat_mask (diff > 1e-6) ensures s_c is not zero for these channels.
    x_dq_novel[:, :, non_flat_mask] = (y_dq[:, :, non_flat_mask] - z_c[non_flat_mask]) / s_c[non_flat_mask]

    # Inverse for flat channels: original value was min_vals (or max_vals, since they are equal).
    # For flat channels, y_dq should ideally be equal to z_c. So (y_dq - z_c) would be 0.
    # We must reconstruct the original constant value directly.
    x_dq_novel[:, :, flat_mask] = min_vals[flat_mask] 
    
    # Calculate memory overhead for s_c and z_c parameters
    mem_overhead_bytes = (s_c.numel() + z_c.numel()) * s_c.element_size()
    
    return x_dq_novel, global_a_scale_novel, mem_overhead_bytes

print("\n--- Applying Novel Channel-wise Min-Max Affine Pre-Quantization ---")
# Quantize Activations using the novel method
x_dq_novel, a_scale_novel, mem_overhead_bytes = channel_wise_affine_quantize_4bit_symmetric(x)
print(f"Activation 4-bit Quantization Scale (Novel, for transformed 'y' tensor): {a_scale_novel:.4f} (Ideal: ~1.0, Good)")
print(f"Memory Overhead for Affine Parameters (s_c, z_c): {mem_overhead_bytes / 1024:.2f} KB")

# Calculate the Novel W4A4 FFN Output
novel_output = x_dq_novel @ W_up_dq

# ---------------------------------------------------------
# Evaluation (The Catastrophe vs. The Solution)
# ---------------------------------------------------------
# Measure how badly the 4-bit quantization destroyed the FFN output
cos_sim_naive = F.cosine_similarity(golden_output.flatten(), w4a4_output_naive.flatten(), dim=0).item()
cos_sim_novel = F.cosine_similarity(golden_output.flatten(), novel_output.flatten(), dim=0).item()

print(f"\n[Results] Naive W4A4 FFN Output Accuracy (Cosine Similarity): {cos_sim_naive * 100:.2f}%")
if cos_sim_naive < 0.90:
    print("\n[FAILURE] As expected, naive W4A4 quantization failed catastrophically.")
    print("The massive outliers in the activation tensor forced the quantization buckets to be too wide.")
    print("Normal token data was crushed to zero. The LLM would hallucinate instantly.")
else:
    print("\n[SUCCESS] Naive W4A4 worked (This should not happen with extreme outliers).")

print(f"\n[Results] Novel W4A4 FFN Output Accuracy (Cosine Similarity): {cos_sim_novel * 100:.2f}%")
if cos_sim_novel > 0.90:
    print("\n[SUCCESS] The Novel Channel-wise Affine Pre-Quantization significantly improved accuracy.")
    print("Outliers are now handled per-channel, allowing for a tight global quantization scale.")
else:
    print("\n[FAILURE] The Novel method did not perform as expected.")

print("\nComparison of Activation Outlier Handling:")
print(f"  Naive Method Global Activation Scale: {a_scale_naive:.4f}")
print(f"  Novel Method Global Activation Scale (for transformed tensor): {a_scale_novel:.4f}")
print(f"  (Ideally, the novel method's scale for the transformed tensor 'y' should be close to 1.0, indicating optimal range utilization.)")
print("=====================================================")