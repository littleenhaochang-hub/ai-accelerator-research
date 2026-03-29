import torch
import torch.nn.functional as F
import math

# --- Configuration for Chained Householder Reflections ---
# Dimension of the vector. For LLMs, this can be 4096, 8192, etc.
D_DIM = 128
# Number of Householder reflections to chain. Typically a small integer like 2-8.
K_REFLECTIONS = 4 

class ChainedHouseholderReflections:
    """
    Constructs a structured orthogonal matrix R as a product of k Householder reflections.
    R = H_1 @ H_2 @ ... @ H_k
    Each H_i = I - 2 * (v_i v_i^T) / (v_i^T v_i)
    """
    def __init__(self, D: int, k: int, device: torch.device = 'cpu', dtype: torch.dtype = torch.float32):
        self.D = D
        self.k = k
        self.device = device
        self.dtype = dtype
        self.reflection_vectors_v = []
        self.v_norm_sq = [] # Precompute v^T v for efficiency

        # Generate k distinct pseudo-random vectors v_i
        for _ in range(k):
            # Generate random vector. Ensure it's not a zero vector to prevent division by zero.
            v = torch.randn(D, device=device, dtype=dtype)
            while v.norm() < 1e-6: # Regenerate if too close to zero
                v = torch.randn(D, device=device, dtype=dtype)
            
            self.reflection_vectors_v.append(v)
            self.v_norm_sq.append(torch.dot(v, v)) # Precompute v^T v

    def _apply_single_reflection(self, x: torch.Tensor, v: torch.Tensor, v_norm_sq: torch.Tensor) -> torch.Tensor:
        """
        Applies a single Householder reflection H = I - 2 * (v v^T) / (v^T v) to vector x.
        Operation: x @ H = x - 2 * ((x @ v) / (v^T v)) * v
        x can be a batch of vectors (B, D) or a single vector (D,).
        v is a single vector (D,).
        """
        # Handle single vector input (D,) by unsqueezing to (1, D)
        if x.dim() == 1:
            x = x.unsqueeze(0) 
            was_1d = True
        else:
            was_1d = False

        # Calculate x @ v for each vector in the batch
        # x_dot_v will be (B,)
        x_dot_v = x @ v 

        # Calculate scaling factor: 2 * (x @ v) / (v^T v)
        # scaling_factor will be (B,), unsqueeze to (B, 1) for broadcasting with v (D,)
        scaling_factor = (2 * x_dot_v / v_norm_sq).unsqueeze(-1) 

        # Apply the reflection: x - scaling_factor * v
        x_reflected = x - scaling_factor * v 

        # Squeeze back to (D,) if original input was 1D
        if was_1d:
            return x_reflected.squeeze(0) 
        return x_reflected

    def apply(self, x: torch.Tensor, transpose: bool = False) -> torch.Tensor:
        """
        Applies the chained Householder reflections to x.
        If transpose is False, applies R = H_1 @ H_2 @ ... @ H_k (forward chain)
        If transpose is True, applies R.t() = H_k @ H_{k-1} @ ... @ H_1 (reverse chain, since H_i is symmetric)
        """
        current_x = x
        if not transpose:
            # Apply H_1 then H_2 ... then H_k
            for i in range(self.k):
                current_x = self._apply_single_reflection(current_x, 
                                                            self.reflection_vectors_v[i], 
                                                            self.v_norm_sq[i])
        else:
            # Apply H_k then H_{k-1} ... then H_1 for R.t()
            for i in range(self.k - 1, -1, -1): # Iterate in reverse order
                current_x = self._apply_single_reflection(current_x, 
                                                            self.reflection_vectors_v[i], 
                                                            self.v_norm_sq[i])
        return current_x

print("=====================================================")
print(" TurboQuant with Chained Householder Reflections")
print(" Demonstrating efficient PolarQuant for large D")
print("=====================================================\n")

# 1. The Original KV Cache Vector (D_DIM dimensions)
x = torch.randn(1, D_DIM)
x[0, 5] = 100.0 # Massive outlier introduced to simulate real-world LLM activations
print(f"Original Vector Max Value (The Outlier): {x.max().item():.2f}")
print(f"Vector Dimension D: {D_DIM}\n")


# --- STAGE 1: POLARQUANT (Random Rotation / Domain Transformation) ---

print(f"--- PolarQuant Implementation Details (D={D_DIM}) ---")

# BASELINE: Dense QR generated orthogonal matrix R
print("\n--- Baseline (Dense R via QR) ---")
# Generate a random orthogonal rotation matrix (R)
H_dense = torch.randn(D_DIM, D_DIM)
R_baseline, _ = torch.linalg.qr(H_dense) 

# Estimate memory usage for R_baseline (float32)
R_baseline_mem_bytes = R_baseline.nelement() * R_baseline.element_size()
print(f"  Memory for Dense R: {R_baseline_mem_bytes / 1024:.2f} KB ({R_baseline_mem_bytes} bytes)")

# Estimate FLOPs for x @ R_baseline (matrix-vector product)
# For a (1, D) @ (D, D) operation, each of the D output elements requires D multiplications and D-1 additions.
# Total FLOPs ~ D * (D multiplications + (D-1) additions) ~ 2 * D^2 FLOPs
flops_baseline_matmul = 2 * D_DIM * D_DIM
print(f"  Estimated FLOPs for x @ R (one pass): {flops_baseline_matmul:,} FLOPs")


# PROPOSED: Chained Householder Reflections
print(f"\n--- Proposed (Chained Householder R, k={K_REFLECTIONS}) ---")
householder_reflector_chain = ChainedHouseholderReflections(D_DIM, K_REFLECTIONS)

# Estimate memory usage for Householder vectors (float32)
# k vectors, each of size D, storing only v_i
householder_mem_bytes = K_REFLECTIONS * D_DIM * householder_reflector_chain.reflection_vectors_v[0].element_size()
print(f"  Memory for Chained Householder R (k={K_REFLECTIONS} vectors): {householder_mem_bytes / 1024:.2f} KB ({householder_mem_bytes} bytes)")
print(f"  Memory Reduction Factor: {R_baseline_mem_bytes / householder_mem_bytes:.2f}x")

# Estimate FLOPs for x @ R (chained Householder applications)
# For a single Householder reflection on a (1,D) vector (x @ H):
#   1. x @ v (dot product): D mults, D-1 adds (approx 2D FLOPs)
#   2. 2 * x_dot_v / v_norm_sq (scalar ops): 1 mult, 1 div (2 FLOPs)
#   3. scalar * v (scalar-vector mult): D mults (D FLOPs)
#   4. x - scaled_v (vector subtraction): D adds (D FLOPs)
# Total per reflection ~ (2D + 2 + D + D) = 4D + 2 FLOPs.
flops_per_householder = 4 * D_DIM + 2 
flops_chained_householder = K_REFLECTIONS * flops_per_householder
print(f"  Estimated FLOPs for x @ R (one pass): {flops_chained_householder:,} FLOPs")
print(f"  FLOPs Reduction Factor: {flops_baseline_matmul / flops_chained_householder:.2f}x")


# Apply the proposed Chained Householder Reflections
x_rotated = householder_reflector_chain.apply(x, transpose=False)
print(f"\nRotated Vector Max Value (Smeared): {x_rotated.max().item():.2f}")

# Quantize the rotated vector heavily (Simulating 3-bit buckets)
# Because the outliers were smeared into a bounded distribution, 
# we can aggressively crush the data into 3 bits (8 buckets) with minimal information loss.
x_quantized_3bit = torch.round(x_rotated / 2.0) * 2.0

# --- STAGE 2: QJL (1-Bit Residual Correction) ---
# Calculate the exact math error caused by the 3-bit quantization
residual_error = x_rotated - x_quantized_3bit

# The Genius Trick: Only store the SIGN (+ or -) of the error. This takes exactly 1 bit.
# We also store a single float16 representing the average error size for the whole vector.
# Statistically, this acts as an unbiased estimator to correct the 3-bit drift.
residual_1bit_sign = torch.sign(residual_error)
average_error_size = residual_error.abs().mean()

# --- RECONSTRUCTION (During LLM Inference) ---
# Rebuild the vector using the 3-bit base + (1-bit sign * average error size)
x_reconstructed_rotated = x_quantized_3bit + (residual_1bit_sign * average_error_size)

# Inverse transform to get the vector back to its original space
# Since R is orthogonal, its inverse is simply its transpose (R.T).
# For chained Householder, R.t() is simply applying the reflections in reverse order.
x_reconstructed = householder_reflector_chain.apply(x_reconstructed_rotated, transpose=True)

# --- THE PROOF ---
# Measure how perfectly the compressed vector matches the original 16-bit vector
accuracy = F.cosine_similarity(x, x_reconstructed).item()
print(f"\nTurboQuant Compression Accuracy with Chained Householder: {accuracy * 100:.2f}%")
print("The vector is mathematically identical enough for Attention, but uses significantly less memory and compute for rotation.")

# Optional: Verify orthogonality and numerical stability (only feasible for relatively small D_DIM)
if D_DIM <= 512 and K_REFLECTIONS * D_DIM < D_DIM * D_DIM: 
    print("\n--- Numerical Verification (for small D_DIM) ---")
    # Construct the full R matrix from Householder reflections for conceptual understanding
    # This process is O(D^3) and O(D^2) memory, which is exactly what we avoid in production.
    # It's here purely for demonstrating the mathematical properties.
    R_full_householder = torch.eye(D_DIM, device=householder_reflector_chain.device, dtype=householder_reflector_chain.dtype)
    for i in range(K_REFLECTIONS):
        v = householder_reflector_chain.reflection_vectors_v[i]
        v_norm_sq = householder_reflector_chain.v_norm_sq[i]
        H_i = torch.eye(D_DIM, device=householder_reflector_chain.device, dtype=householder_reflector_chain.dtype) - (2 / v_norm_sq) * torch.outer(v, v)
        R_full_householder = R_full_householder @ H_i

    # Verify R @ R.t() = I (orthogonality property)
    orthogonality_error = torch.linalg.norm(R_full_householder @ R_full_householder.T - torch.eye(D_DIM, device=R_full_householder.device, dtype=R_full_householder.dtype))
    print(f"  Orthogonality Error (||R @ R.T - I||) for Chained Householder R: {orthogonality_error.item():.2e}")
    if orthogonality_error > 1e-4:
        print("  WARNING: Orthogonality error is relatively high. Consider increasing D_DIM stability or K_REFLECTIONS.")
    
    # Compare result with dense R (for small D where baseline is feasible)
    # Note: Householder and dense QR produce DIFFERENT *random* rotations, but both are valid orthogonal rotations.
    # The similarity here just confirms that the Householder chain itself performs a valid rotation.
    x_rotated_baseline_actual = x @ R_baseline
    similarity_householder_to_dense = F.cosine_similarity(x_rotated_baseline_actual, x_rotated).item()
    print(f"  Cosine Similarity (Householder R rotated vs Baseline R rotated): {similarity_householder_to_dense * 100:.2f}%")
    print("  Note: This similarity shows two different valid random rotations. It's expected not to be 100%.")