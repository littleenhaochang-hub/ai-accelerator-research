import torch
import torch.nn as nn
import torch.nn.functional as F
import math

# Using a consistent print separator
def print_separator(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

print_separator("W4A4 Quantization Baseline for LLM FFN Layers")
print("Goal: Simulate catastrophic failure of 4-bit activation quantization")
print("      due to massive outliers in Feed-Forward Networks, then fix with AGOR.\n")

# 1. Simulation Setup (LLaMA-style FFN Layer)
# Batch=1, SeqLen=1024, Hidden Dim=4096, Intermediate Dim=11008
B, S, D, I = 1, 1024, 4096, 11008

print(f"Simulating FFN Activation Tensor: [Batch:{B}, SeqLen:{S}, Dim:{D}]")

# Simulate Activation Input (X) with massive outliers
# LLM activations typically have a few channels with values 100x larger than the mean
x = torch.randn(B, S, D, dtype=torch.float32) * 0.1
# Inject massive outliers into specific channels (e.g., channel 10 and 100)
# These outliers affect all elements in that specific channel across batch and sequence length
x[:, :, 10] = 50.0
x[:, :, 100] = -45.0
# Add another type of outlier that might be missed by simple std dev for robustness testing
x[:, :, 200] = 3.0 # A smaller but still large outlier compared to 0.1
x[:, :, 300] = -2.5

print(f"Original Activation Max Value (Outlier): {x.max().item():.2f}")
print(f"Original Activation Min Value (Outlier): {x.min().item():.2f}")
print(f"Original Activation Mean: {x.mean().item():.4f}")
print(f"Original Activation Std Dev: {x.std().item():.4f}")


# Simulate FFN Up-Projection Weight (W)
# Weights are usually well-behaved Gaussian, easy to quantize
W_up = torch.randn(D, I, dtype=torch.float32) * 0.02

# ---------------------------------------------------------
# The Golden Standard (FP32/FP16 Math)
# ---------------------------------------------------------
# This is what the LLM expects the FFN output to look like
golden_output = x @ W_up

print_separator("Applying Naive W4A4 Quantization")

def quantize_4bit_symmetric(tensor):
    """
    Standard symmetric 4-bit uniform quantization.
    Maps floating point to integers [-8, 7].
    """
    qmax = 7.0
    
    scale = tensor.abs().max() / qmax
    
    x_q = torch.clamp(torch.round(tensor / scale), -8.0, 7.0)
    
    x_dq = x_q * scale
    return x_dq, scale

# Quantize Weights to 4-bit
W_up_dq, w_scale = quantize_4bit_symmetric(W_up)
print(f"Weight 4-bit Quantization Scale: {w_scale:.4f} (Small, Good)")

# Quantize Activations to 4-bit
x_dq_naive, a_scale_naive = quantize_4bit_symmetric(x)
print(f"Activation 4-bit Quantization Scale (Naive): {a_scale_naive:.4f} (Massive, BAD)")

# Calculate the W4A4 FFN Output
w4a4_output_naive = x_dq_naive @ W_up_dq

# ---------------------------------------------------------
# Adaptive Group-wise Outlier Retention (AGOR) Quantization
# ---------------------------------------------------------
print_separator("Applying AGOR Quantization for Activations")

def quantize_agor(tensor, group_size=64, outlier_threshold_std_multiplier=3.0, outlier_std_percentile_cutoff=0.995, outlier_precision=torch.float16, int4_qmax=7.0):
    """
    Adaptive Group-wise Outlier Retention (AGOR) for activations.
    Quantizes activations in small, independent groups of channels.
    Identifies extreme outliers, retains them in higher precision (FP16),
    and quantizes remaining 'normal' values to INT4 using a scale derived
    only from non-outlier values.

    Args:
        tensor (torch.Tensor): The activation tensor (B, S, D).
        group_size (int): Number of channels per group.
        outlier_threshold_std_multiplier (float): Multiplier for the robust std
                                                  to determine the outlier threshold.
        outlier_std_percentile_cutoff (float): Percentile to use for calculating the robust std
                                                (e.g., 0.995 means consider values up to 99.5th percentile).
        outlier_precision (torch.dtype): Data type for retained outliers (e.g., torch.float16).
        int4_qmax (float): Maximum absolute integer value for INT4 quantization (e.g., 7.0).

    Returns:
        torch.Tensor: Reconstructed FP32 tensor after AGOR quantization.
        dict: Metrics including memory usage, outlier counts, and effective bitwidth.
    """
    B, S, D = tensor.shape

    reconstructed_tensor = torch.zeros_like(tensor, dtype=torch.float32)

    total_elements = B * S * D
    num_outliers = 0
    total_memory_agor_bytes = 0 

    for group_start in range(0, D, group_size):
        group_end = min(group_start + group_size, D)
        group_slice = slice(group_start, group_end)
        group_tensor = tensor[:, :, group_slice] # Shape (B, S, actual_group_size)

        current_group_elements = group_tensor.numel()
        if current_group_elements == 0:
            continue

        flat_group = group_tensor.flatten()

        # Step 1: Calculate a robust standard deviation for the group
        # This prevents extreme outliers from inflating the std used for thresholding
        
        if current_group_elements <= 1: 
            # If group has 0 or 1 element, std is undefined or 0.
            # No meaningful outliers to detect in such a small group.
            reconstructed_tensor[:, :, group_slice] = group_tensor # Keep original precision
            total_memory_agor_bytes += current_group_elements * 4 
            continue
        
        # Sort absolute values to estimate std of "normal" values
        sorted_abs_group = flat_group.abs().sort().values
        # Define upper bound for "normal" values based on a percentile
        upper_bound_idx = min(math.ceil(current_group_elements * outlier_std_percentile_cutoff) - 1, current_group_elements - 1)
        upper_bound_idx = max(0, upper_bound_idx) # Ensure index is not negative

        # Extract the subset of "normal" values for robust std calculation
        subset_for_std = sorted_abs_group[:upper_bound_idx+1]
        
        if subset_for_std.numel() <= 1 or subset_for_std.max() - subset_for_std.min() < 1e-6:
            # If subset is too small or all values are identical (range is effectively zero), 
            # use max value as a proxy for scale or a default small value if max is zero.
            current_group_std_robust = subset_for_std.max().item() if subset_for_std.numel() > 0 and subset_for_std.max().item() > 1e-6 else 1.0
        else:
            current_group_std_robust = subset_for_std.std().item()

        # Step 2: Define outlier threshold using the robust standard deviation
        outlier_threshold = outlier_threshold_std_multiplier * current_group_std_robust

        # Step 3: Identify outliers using the calculated threshold
        outliers_mask = group_tensor.abs() > outlier_threshold

        # Store outliers in higher precision (FP16)
        outliers = group_tensor[outliers_mask].to(outlier_precision)
        
        # Extract normal values (non-outliers)
        normal_values = group_tensor[~outliers_mask]

        # Quantize normal values to INT4
        x_dq_normal = torch.empty(0, dtype=torch.float32, device=tensor.device) 
        if normal_values.numel() > 0:
            # Calculate scale *only* from normal values
            normal_abs_max = normal_values.abs().max()
            if normal_abs_max == 0:
                normal_scale = 1e-6 # A tiny scale to avoid division by zero if all non-outliers are zero
            else:
                normal_scale = normal_abs_max / int4_qmax
            
            x_q_normal = torch.clamp(torch.round(normal_values / normal_scale), -8.0, 7.0)
            x_dq_normal = x_q_normal * normal_scale
        
        # Step 4: Reconstruct the group tensor in FP32
        temp_reconstructed_group = torch.zeros_like(group_tensor, dtype=torch.float32)
        
        if x_dq_normal.numel() > 0:
            temp_reconstructed_group[~outliers_mask] = x_dq_normal
        
        if outliers.numel() > 0:
            temp_reconstructed_group[outliers_mask] = outliers.to(torch.float32)
        
        reconstructed_tensor[:, :, group_slice] = temp_reconstructed_group

        # Accumulate metrics
        num_outliers += outliers.numel()

        # Estimate memory usage for this group (in bytes)
        total_memory_agor_bytes += math.ceil(normal_values.numel() / 2.0) # INT4 part (0.5 bytes/value)
        total_memory_agor_bytes += outliers.numel() * 2 # FP16 part (2 bytes/value)
        total_memory_agor_bytes += math.ceil(current_group_elements / 8.0) # Bitmask (1 bit/value)
        total_memory_agor_bytes += 4 # Scale (1 FP32 scale per group)

    # Final memory and bitwidth calculations
    total_memory_original_bytes = total_elements * 4 # FP32 = 4 bytes
    
    effective_bitwidth = (total_memory_agor_bytes * 8) / total_elements if total_elements > 0 else 0

    agor_metrics = {
        "num_outliers": num_outliers,
        "outlier_percentage": (num_outliers / total_elements * 100) if total_elements > 0 else 0,
        "total_memory_agor_bytes": total_memory_agor_bytes,
        "total_memory_original_bytes": total_memory_original_bytes,
        "effective_bitwidth": effective_bitwidth,
        "memory_savings_ratio": (total_memory_original_bytes / total_memory_agor_bytes) if total_memory_agor_bytes > 0 else float('inf')
    }

    return reconstructed_tensor, agor_metrics

# Parameters for AGOR
AGOR_GROUP_SIZE = 64 # Channels per group (e.g., D=4096, 64 groups)
AGOR_OUTLIER_STD_MULTIPLIER = 3.0 # Multiplier for robust_std to identify outliers
AGOR_OUTLIER_STD_PERCENTILE_CUTOFF = 0.995 # Calculate robust std using values up to this percentile
AGOR_OUTLIER_PRECISION = torch.float16 # Precision for retained outliers

x_agor_dq, agor_metrics = quantize_agor(
    x, 
    group_size=AGOR_GROUP_SIZE,
    outlier_threshold_std_multiplier=AGOR_OUTLIER_STD_MULTIPLIER,
    outlier_std_percentile_cutoff=AGOR_OUTLIER_STD_PERCENTILE_CUTOFF,
    outlier_precision=AGOR_OUTLIER_PRECISION
)

print(f"AGOR Group Size: {AGOR_GROUP_SIZE}")
print(f"AGOR Outlier Threshold (robust std multiplier): {AGOR_OUTLIER_STD_MULTIPLIER}")
print(f"AGOR Robust Std Percentile Cutoff: {AGOR_OUTLIER_STD_PERCENTILE_CUTOFF}")
print(f"AGOR Outlier Precision: {str(AGOR_OUTLIER_PRECISION).split('.')[-1]}")
print(f"Number of Outliers Detected: {agor_metrics['num_outliers']:,}")
print(f"Outlier Percentage: {agor_metrics['outlier_percentage']:.4f}%")
print(f"Estimated AGOR Memory Footprint: {agor_metrics['total_memory_agor_bytes'] / (1024*1024):.2f} MB")
print(f"Original FP32 Memory Footprint: {agor_metrics['total_memory_original_bytes'] / (1024*1024):.2f} MB")
print(f"Estimated Memory Savings Ratio (FP32 / AGOR): {agor_metrics['memory_savings_ratio']:.2f}x")
print(f"Estimated Effective Average Bitwidth: {agor_metrics['effective_bitwidth']:.2f} bits/value")

# Calculate the AGOR W4A4 FFN Output (Weights are W4, Activations are AGOR)
w4a4_output_agor = x_agor_dq @ W_up_dq

# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------
print_separator("Evaluation Results")

# Naive W4A4 Evaluation
cos_sim_naive = F.cosine_similarity(golden_output.flatten(), w4a4_output_naive.flatten(), dim=0).item()
print(f"[Results] Naive W4A4 FFN Output Accuracy (Cosine Similarity): {cos_sim_naive * 100:.2f}%")

if cos_sim_naive < 0.90:
    print("[FAILURE] As expected, naive W4A4 quantization failed catastrophically.")
    print("The massive outliers in the activation tensor forced the quantization buckets to be too wide.")
    print("Normal token data was crushed to zero. The LLM would hallucinate instantly.")
else:
    print("[SUCCESS] Naive W4A4 worked (This should not happen with extreme outliers).")

# AGOR W4A4 Evaluation
cos_sim_agor = F.cosine_similarity(golden_output.flatten(), w4a4_output_agor.flatten(), dim=0).item()
print(f"\n[Results] AGOR W4A4 FFN Output Accuracy (Cosine Similarity): {cos_sim_agor * 100:.2f}%")

if cos_sim_agor > cos_sim_naive + 0.05: # A significant improvement
    print(f"[SUCCESS] AGOR improved accuracy significantly compared to naive W4A4. (Improvement: {(cos_sim_agor - cos_sim_naive)*100:.2f}%)")
    print("AGOR successfully preserved critical information from outliers, leading to better FFN output.")
    print("The adaptive grouping and separate retention of outliers mitigated catastrophic information loss.")
elif cos_sim_agor > 0.95:
    print("[SUCCESS] AGOR achieved high accuracy, successfully preserving critical information.")
else:
    print("[MIXED] AGOR results were not as good as expected or only marginally better.")


# Additional metric: L2 norm difference from golden
l2_diff_naive = (golden_output - w4a4_output_naive).pow(2).mean().sqrt().item()
l2_diff_agor = (golden_output - w4a4_output_agor).pow(2).mean().sqrt().item()

print(f"\nL2 Norm Difference (Golden vs Naive W4A4): {l2_diff_naive:.4f}")
print(f"L2 Norm Difference (Golden vs AGOR W4A4): {l2_diff_agor:.4f}")

if l2_diff_agor < l2_diff_naive:
    print("[SUCCESS] AGOR also shows reduced L2 norm difference, indicating closer approximation to golden output.")
else:
    print("[MIXED] L2 norm difference for AGOR is not lower than naive, which is unexpected.")

print_separator("Latency and Hardware Considerations (Simulated Discussion)")
print("AGOR introduces computational overhead for outlier detection, separation, and reconstruction.")
print("However, this is typically amortized by specialized hardware units (e.g., in an NPU/TPU) that can perform these operations efficiently in parallel.")
print("The primary benefit is enabling significantly higher memory compression (lower bitwidth) for the majority of activations, reducing memory bandwidth bottlenecks.")
print("The hybrid INT4/FP8 (or INT4/FP16) matrix multiplication itself would require specialized hardware support, but it allows preserving critical information while still leveraging dense low-bit computation.")
print(f"With an average effective bitwidth of {agor_metrics['effective_bitwidth']:.2f} bits/value, AGOR offers a compelling trade-off between memory efficiency and accuracy.")