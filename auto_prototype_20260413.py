import torch
import math

# --- Configuration ---
BATCH_SIZE = 1
SEQUENCE_LENGTH = 4096 # Simulates a 4K context
HIDDEN_DIM = 4096      # Typical hidden dimension for large models (e.g., LLaMA-like)
LOW_RANK_K = 64        # Hyperparameter: Rank for the low-rank approximation (co-design choice)
DTYPE = torch.bfloat16 # Simulating typical activation precision on edge devices

# --- Simulate an activation tensor (reshaped for SVD) ---
# A typical activation tensor would be (BATCH_SIZE, SEQUENCE_LENGTH, HIDDEN_DIM).
# For SVD, we flatten BATCH_SIZE and SEQUENCE_LENGTH dimensions into N.
N = BATCH_SIZE * SEQUENCE_LENGTH
D = HIDDEN_DIM
original_activation = torch.randn(N, D, dtype=DTYPE)

# --- Software Part: Activation Sketching (SVD-based Low-Rank Approximation) ---
# This simulates storing a compressed "sketch" of the activation during the forward pass.
U, S, Vh = torch.linalg.svd(original_activation, full_matrices=False)

# Select top K singular values and corresponding vectors for low-rank approximation
U_k = U[:, :LOW_RANK_K]
S_k = S[:LOW_RANK_K]
Vh_k = Vh[:LOW_RANK_K, :]

# --- Memory Analysis (Software benefit: SRAM reduction) ---
original_memory_bytes = original_activation.numel() * torch.finfo(DTYPE).bits / 8
sketch_memory_bytes = (U_k.numel() + S_k.numel() + Vh_k.numel()) * torch.finfo(DTYPE).bits / 8

memory_reduction_ratio = original_memory_bytes / sketch_memory_bytes
memory_reduction_percentage = (1 - (sketch_memory_bytes / original_memory_bytes)) * 100

print(f"--- Forward Activation Memory Wall Solution Prototype ---")
print(f"Context: {SEQUENCE_LENGTH} (Sequence Length), {HIDDEN_DIM} (Hidden Dim)")
print(f"Activation Tensor Shape (flattened): {N}x{D} ({DTYPE})")
print(f"Original Memory per Activation: {original_memory_bytes / (1024**2):.2f} MB")
print(f"Sketch Memory (Rank {LOW_RANK_K}): {sketch_memory_bytes / (1024**2):.2f} MB")
print(f"Memory Reduction: {memory_reduction_ratio:.2f}x ({memory_reduction_percentage:.2f}%)")

# --- Hardware Part: On-Chip Recomputation Unit (during backward pass) ---
# This simulates reconstructing the full activation from its sketch on demand.
# A dedicated hardware unit could perform this efficiently.
reconstructed_activation = U_k @ torch.diag_embed(S_k) @ Vh_k

# --- FLOPs Analysis (Hardware cost for recomputation) ---
# Recomputation FLOPs for A_k = U_k @ diag(S_k) @ Vh_k
# U_k @ diag(S_k): (N, k) @ (k, k) -> (N, k). FLOPs: N * k * k
# (Result) @ Vh_k: (N, k) @ (k, D) -> (N, D). FLOPs: N * k * D
recomputation_flops = N * LOW_RANK_K * LOW_RANK_K + N * LOW_RANK_K * D

print(f"Recomputation FLOPs (on-chip): {recomputation_flops / 1e9:.2f} GFLOPs")

# --- Fidelity Analysis (SQNR - Signal-to-Quantization Noise Ratio) ---
# Measures how well the reconstructed activation approximates the original.
diff = original_activation - reconstructed_activation
mse = torch.mean(diff**2).item()
power_orig = torch.mean(original_activation**2).item()
sqnr = 10 * math.log10(power_orig / mse) if mse > 1e-9 else float('inf')

print(f"Signal-to-Noise Ratio (SQNR): {sqnr:.2f} dB")

# --- Verdict ---
# Thresholds are indicative for demonstrating potential.
if sqnr > 35 and memory_reduction_ratio > 10 and recomputation_flops < 2e9:
    verdict = "Verdict: HIGHLY PROMISING. Significant memory savings, high fidelity, and moderate recomputation cost for a dedicated unit. This approach directly addresses the Forward Activation Memory Wall by trading on-chip recomputation for SRAM."
elif sqnr > 25 and memory_reduction_ratio > 5:
    verdict = "Verdict: PROMISING. Good memory savings and fidelity, recomputation cost may require further hardware optimization."
else:
    verdict = "Verdict: FURTHER RESEARCH NEEDED. Trade-offs between memory, recomputation, and fidelity are critical for practical deployment."

print(f"\n{verdict}")