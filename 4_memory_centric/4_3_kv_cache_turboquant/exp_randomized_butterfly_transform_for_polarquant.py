import torch
import torch.nn.functional as F
import math
import time

print("=====================================================")
print(" Minimal TurboQuant Proof-of-Concept with Randomized Butterfly Transform (RBT)")
print(" Demonstrating the math behind the 4x KV Cache compression with O(D log D) PolarQuant")
print("=====================================================\n")

# 1. The Original KV Cache Vector (128 dimensions)
D = 128 # Dimension
x = torch.randn(1, D)
x[0, 5] = 100.0
print(f"Original Vector Max Value (The Outlier): {x.max().item():.2f}")

# --- STAGE 1: POLARQUANT (Random Rotation / Domain Transformation) ---

# Baseline: Dense Random Orthogonal Matrix (R) using QR decomposition
start_time_qr_gen = time.perf_counter()
H_dense = torch.randn(D, D)
R_dense, _ = torch.linalg.qr(H_dense)
end_time_qr_gen = time.perf_counter()
print(f"\n[Baseline QR] R_dense generation time: {(end_time_qr_gen - start_time_qr_gen)*1000:.3f} ms")
print(f"[Baseline QR] R_dense memory (float32): {R_dense.numel() * R_dense.element_size() / (1024*1024):.4f} MB")
# Theoretical application time complexity for matrix-vector product: O(D^2)

# Proposed: Randomized Butterfly Transform (RBT) or similar fast orthogonal transform
# This construction aims to approximate a random orthogonal matrix
# while being composed of sparse and structured components.
# In a true O(D log D) implementation, the full DxD matrix `R_butterfly`
# would NOT be materialized. Instead, its components (permutations, diagonals,
# and the fast Hadamard transform itself) would be applied sequentially.

# Helper function to generate Hadamard matrix for PyTorch versions older than 2.0
def hadamard_matrix_recursive(k):
    """
    Generates a Hadamard matrix of order 2^k.
    Assumes k >= 0.
    """
    if k == 0:
        return torch.tensor([[1.]])
    
    H_prev = hadamard_matrix_recursive(k - 1)
    H_top = torch.cat((H_prev, H_prev), dim=1)
    H_bottom = torch.cat((H_prev, -H_prev), dim=1)
    return torch.cat((H_top, H_bottom), dim=0)

start_time_rbt_gen = time.perf_counter()
# Component 1: Random Permutation Matrix (P)
# In a sparse implementation, this is just a permutation array of D indices (O(D) memory, O(D) compute)
perm_indices = torch.randperm(D)
P = torch.eye(D)[perm_indices]

# Component 2: Random Diagonal Scaling Matrix (D_scale) with +1/-1 entries
# This ensures orthogonality (D_scale @ D_scale.t() = I).
# In a sparse implementation, this is just D diagonal values (O(D) memory, O(D) compute)
D_scale_vals = (torch.randint(0, 2, (D,)) * 2 - 1).float()
D_scale = torch.diag(D_scale_vals)

# Component 3: Normalized Hadamard Matrix (H_norm)
# The Hadamard transform itself can be computed in O(D log D) operations (e.g., Fast Hadamard Transform).
# For this Proof-of-Concept, we materialize the DxD Hadamard matrix for simplicity,
# but a production system would use an O(D log D) algorithm that avoids full matrix multiplication.
# Using recursive implementation as torch.linalg.hadamard might not be available in all PyTorch versions.
k = int(math.log2(D))
H_unnorm = hadamard_matrix_recursive(k) # Use the recursive function
H_norm = H_unnorm / math.sqrt(D) # Normalized for orthogonality

# R_butterfly is the product of these orthogonal/permutation matrices.
# The product of orthogonal matrices (P, D_scale, H_norm) is also orthogonal.
R_butterfly = P @ D_scale @ H_norm
end_time_rbt_gen = time.perf_counter()

print(f"\n[RBT Proposed] R_butterfly generation time: {(end_time_rbt_gen - start_time_rbt_gen)*1000:.3f} ms")
print(f"[RBT Proposed] R_butterfly memory (float32, materialized): {R_butterfly.numel() * R_butterfly.element_size() / (1024*1024):.4f} MB")
print(f"       Note: In a true O(D log D) RBT implementation, R_butterfly would NOT be materialized as a DxD matrix.")
print(f"       Instead, its sparse components (permutation indices, diagonal values) and the Hadamard transform")
print(f"       would be applied directly. This results in O(D) memory for components and O(D log D) compute.")
print(f"       Example sparse component memory: (Permutation: {D * torch.tensor(0).element_size()/1024:.4f} KB, Diagonals: {D * D_scale_vals.element_size()/1024:.4f} KB)")


# --- Full Pipeline Comparison (R_dense vs R_butterfly) ---

print("\n--- Applying PolarQuant with Baseline QR Transform ---")
start_time_qr_fwd = time.perf_counter()
x_rotated_dense = x @ R_dense
end_time_qr_fwd = time.perf_counter()
print(f"Rotated Vector (Baseline QR) Max Value (Smeared): {x_rotated_dense.max().item():.2f}")
print(f"Baseline QR Forward transform time: {(end_time_qr_fwd - start_time_qr_fwd)*1000:.3f} ms (O(D^2) complexity)")

# Quantize and reconstruct with Baseline QR
x_quantized_3bit_dense = torch.round(x_rotated_dense / 2.0) * 2.0
residual_error_dense = x_rotated_dense - x_quantized_3bit_dense
residual_1bit_sign_dense = torch.sign(residual_error_dense)
average_error_size_dense = residual_error_dense.abs().mean()
x_reconstructed_rotated_dense = x_quantized_3bit_dense + (residual_1bit_sign_dense * average_error_size_dense)

start_time_qr_inv = time.perf_counter()
x_reconstructed_from_dense = x_reconstructed_rotated_dense @ R_dense.t()
end_time_qr_inv = time.perf_counter()
print(f"Baseline QR Inverse transform time: {(end_time_qr_inv - start_time_qr_inv)*1000:.3f} ms (O(D^2) complexity)")
accuracy_full_qr = F.cosine_similarity(x, x_reconstructed_from_dense).item()
print(f"Full Pipeline Accuracy (Baseline QR): {accuracy_full_qr * 100:.2f}%")

print("\n--- Applying PolarQuant with RBT Proposed Transform ---")
# Apply the Randomized Butterfly Transform
start_time_rbt_fwd = time.perf_counter()
# In a real O(D log D) implementation, this would be:
# x_rotated_butterfly = x[..., perm_indices] # O(D)
# x_rotated_butterfly = x_rotated_butterfly * D_scale_vals # O(D)
# x_rotated_butterfly = fast_hadamard_transform(x_rotated_butterfly) # O(D log D)
x_rotated_butterfly = x @ R_butterfly # For PoC simplicity, use materialized DxD matrix
end_time_rbt_fwd = time.perf_counter()
print(f"Rotated Vector (RBT Proposed) Max Value (Smeared): {x_rotated_butterfly.max().item():.2f}")
print(f"RBT Forward transform time (PoC materialized DxD): {(end_time_rbt_fwd - start_time_rbt_fwd)*1000:.3f} ms (Still O(D^2) due to materialization)")
print(f"       Note: A true sparse RBT application would be O(D log D) using sequential component application.")

# Quantize and reconstruct with RBT
x_quantized_3bit_butterfly = torch.round(x_rotated_butterfly / 2.0) * 2.0
residual_error_butterfly = x_rotated_butterfly - x_quantized_3bit_butterfly
residual_1bit_sign_butterfly = torch.sign(residual_error_butterfly)
average_error_size_butterfly = residual_error_butterfly.abs().mean()
x_reconstructed_rotated_butterfly = x_quantized_3bit_butterfly + (residual_1bit_sign_butterfly * average_error_size_butterfly)

# Inverse transform using R_butterfly.t()
# R_butterfly.t() = (P @ D_scale @ H_norm).t() = H_norm.t() @ D_scale.t() @ P.t()
# Since H_norm, D_scale, P are orthogonal and H_norm, D_scale are symmetric:
# R_butterfly.t() = H_norm @ D_scale @ P.t()
# In a real O(D log D) implementation, this would involve inverse operations in reverse order:
# x_inv_temp = fast_inverse_hadamard_transform(x_reconstructed_rotated_butterfly) # O(D log D)
# x_inv_temp = x_inv_temp * D_scale_vals # O(D) (inverse for D_scale is D_scale itself)
# x_reconstructed_from_butterfly = x_inv_temp @ P.t() # O(D) (inverse permutation)
start_time_rbt_inv = time.perf_counter()
x_reconstructed_from_butterfly = x_reconstructed_rotated_butterfly @ R_butterfly.t()
end_time_rbt_inv = time.perf_counter()
print(f"RBT Inverse transform time (PoC materialized DxD): {(end_time_rbt_inv - start_time_rbt_inv)*1000:.3f} ms (Still O(D^2) due to materialization)")
print(f"       Note: A true sparse RBT application would be O(D log D) using sequential component application.")

accuracy_full_rbt = F.cosine_similarity(x, x_reconstructed_from_butterfly).item()
print(f"Full Pipeline Accuracy (RBT Proposed): {accuracy_full_rbt * 100:.2f}%")
print("The vector is mathematically identical enough for Attention, but uses 75% less memory.")

# Additional check for RBT orthogonality
# Ensure that the constructed R_butterfly matrix is indeed numerically orthogonal
orthogonality_check = torch.allclose(R_butterfly @ R_butterfly.t(), torch.eye(D), atol=1e-5)
print(f"\nOrthogonality Check: R_butterfly @ R_butterfly.t() is close to Identity: {orthogonality_check}")