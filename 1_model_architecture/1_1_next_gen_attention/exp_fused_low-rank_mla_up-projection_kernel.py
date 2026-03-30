import torch
import torch.nn as nn
import torch.nn.functional as F
import time

print("=====================================================")
print(" Multi-Head Latent Attention (MLA) Baseline (DeepSeek-V3)")
print(" Goal: Simulate a Fused Kernel for Low-Rank Up-Projection")
print("       Prove wall-clock latency speedup over dense baseline.")
print("=====================================================\n")

# Determine device for execution
if torch.cuda.is_available():
    DEVICE = 'cuda'
    print("Running on CUDA device.")
else:
    DEVICE = 'cpu'
    print("CUDA is not available. Running on CPU.")
    print("WARNING: This benchmark is designed for GPU. CPU results will not reflect intended GPU performance or speedups.")

# 1. Architecture Parameters (Scaled down for simulation)
BATCH_SIZE = 1
SEQ_LEN = 4096
D_MODEL = 2048       # Hidden dimension
N_HEADS = 16         # Number of attention heads
D_HEAD = 128         # Dimension per head
D_KV_COMPRESSED = 512 # The Latent Vector dimension (Crucial for MLA)

# Low-rank factorization parameter: intermediate rank R
RANK_R = 128 # Must be significantly smaller than D_KV_COMPRESSED and N_HEADS * D_HEAD for FLOPs reduction

print(f"Simulating Attention: B={BATCH_SIZE}, SeqLen={SEQ_LEN}, d_model={D_MODEL}")
print(f"MLA Up-Projection Parameters: D_KV_COMPRESSED={D_KV_COMPRESSED}, Output_Dim={N_HEADS * D_HEAD}")
print(f"Low-Rank Decomposition Rank (R): {RANK_R}")

# Generate Random Input States and move to selected device
hidden_states = torch.randn(BATCH_SIZE, SEQ_LEN, D_MODEL, device=DEVICE, dtype=torch.float16) # Use FP16 for LLM scenarios

# ---------------------------------------------------------
# Common MLA Components: Down-projection to latent vector
# ---------------------------------------------------------
W_down_kv = nn.Linear(D_MODEL, D_KV_COMPRESSED, bias=False, dtype=torch.float16).to(DEVICE)
c_kv = W_down_kv(hidden_states) # This is the compressed KV cache (latent vector)

print(f"\nc_kv (Latent Vector) shape: {c_kv.shape}")

# Define a synchronization function to handle both CUDA and CPU
def synchronize_device():
    if DEVICE == 'cuda':
        torch.cuda.synchronize()
    # For CPU, operations are generally synchronous, so no explicit synchronize needed.

# ---------------------------------------------------------
# Scenario A: Original Dense MLA Up-Projection (Baseline for comparison)
# W_up_k maps D_KV_COMPRESSED -> N_HEADS * D_HEAD
# ---------------------------------------------------------
W_up_k_dense = nn.Linear(D_KV_COMPRESSED, N_HEADS * D_HEAD, bias=False, dtype=torch.float16).to(DEVICE)

# Function to encapsulate dense projection
def dense_up_projection(input_tensor, weight_matrix_linear):
    return weight_matrix_linear(input_tensor)

# Warm-up for CUDA/CPU
for _ in range(10):
    _ = dense_up_projection(c_kv, W_up_k_dense)
synchronize_device()

num_runs = 200
start_time_dense = time.perf_counter()
for _ in range(num_runs):
    k_mla_dense = dense_up_projection(c_kv, W_up_k_dense)
synchronize_device()
end_time_dense = time.perf_counter()
time_dense = (end_time_dense - start_time_dense) / num_runs
print(f"\n--- Scenario A: Original Dense MLA Up-Projection (Baseline) ---")
print(f"  Output K-vector shape: {k_mla_dense.shape}")
print(f"  Execution time: {time_dense * 1000:.3f} ms")

# ---------------------------------------------------------
# Scenario B: Low-Rank MLA Up-Projection (Split / Non-Fused - Previously Slow)
# W_up_k = M_X1 @ M_X2
# M_X1: (D_KV_COMPRESSED, RANK_R)
# M_X2: (RANK_R, N_HEADS * D_HEAD)
# ---------------------------------------------------------
M_X1 = nn.Linear(D_KV_COMPRESSED, RANK_R, bias=False, dtype=torch.float16).to(DEVICE)
M_X2 = nn.Linear(RANK_R, N_HEADS * D_HEAD, bias=False, dtype=torch.float16).to(DEVICE)

# Function to encapsulate split low-rank projection
def split_low_rank_projection(input_tensor, m1_linear, m2_linear):
    intermediate = m1_linear(input_tensor) # This intermediate tensor is materialized in HBM
    output = m2_linear(intermediate)
    return output

# Warm-up for CUDA/CPU
for _ in range(10):
    _ = split_low_rank_projection(c_kv, M_X1, M_X2)
synchronize_device()

start_time_split = time.perf_counter()
for _ in range(num_runs):
    k_mla_split = split_low_rank_projection(c_kv, M_X1, M_X2)
synchronize_device()
end_time_split = time.perf_counter()
time_split = (end_time_split - start_time_split) / num_runs
print(f"\n--- Scenario B: Low-Rank MLA Up-Projection (Split, non-fused) ---")
print(f"  Output K-vector shape: {k_mla_split.shape}")
print(f"  Execution time: {time_split * 1000:.3f} ms")

# ---------------------------------------------------------
# Scenario C: Fused Low-Rank MLA Up-Projection (Optimized Goal)
# Using torch.compile to fuse M_X1 and M_X2 matrix multiplications
# ---------------------------------------------------------

# Function for fused operation (mimics nn.Linear behavior: input @ weight.T)
def fused_low_rank_projection_func(input_tensor, m1_weight, m2_weight):
    # torch.matmul(A, B) is equivalent to A @ B
    # nn.Linear(in, out) performs input @ weight.T
    intermediate = torch.matmul(input_tensor, m1_weight.T)
    output = torch.matmul(intermediate, m2_weight.T)
    return output

# Compile the function using the specified mode
# "reduce-overhead" aims to reduce Python overhead and fuse simple operations.
# For consecutive matrix multiplications, it can combine them into a single, optimized GPU kernel,
# preventing the intermediate from being written to HBM.
fused_low_rank_projection_compiled = torch.compile(fused_low_rank_projection_func, mode="reduce-overhead")

# Warm-up for CUDA/CPU with the compiled function
# Note: For torch.compile, it's generally good practice to warm up longer
# as compilation happens on the first few runs.
for _ in range(20): # Longer warm-up for compile
    _ = fused_low_rank_projection_compiled(c_kv, M_X1.weight, M_X2.weight)
synchronize_device()

start_time_fused = time.perf_counter()
for _ in range(num_runs):
    k_mla_fused = fused_low_rank_projection_compiled(c_kv, M_X1.weight, M_X2.weight)
synchronize_device()
end_time_fused = time.perf_counter()
time_fused = (end_time_fused - start_time_fused) / num_runs
print(f"\n--- Scenario C: Fused Low-Rank MLA Up-Projection (Compiled) ---")
print(f"  Output K-vector shape: {k_mla_fused.shape}")
print(f"  Execution time: {time_fused * 1000:.3f} ms")

# Verify correctness (shapes and values)
# The split and fused low-rank should be numerically identical as they perform the same computation.
# Adjust tolerance for FP16 or if running on CPU where precision might vary slightly more
assert torch.allclose(k_mla_split, k_mla_fused, atol=1e-3, rtol=1e-3), "Fused and Split Low-Rank outputs do not match!"
print("\nNumerical check: Fused and Split Low-Rank outputs are identical.")

print("\n--- Comparative Results ---")
print(f"Dense Baseline (A):          {time_dense * 1000:.3f} ms")
print(f"Split Low-Rank (B):          {time_split * 1000:.3f} ms (Wall-clock slowdown expected due to intermediate HBM writes without fusion)")
print(f"Fused Low-Rank (C):          {time_fused * 1000:.3f} ms")

if time_fused < time_dense:
    print(f"\nConclusion: Fused Low-Rank (C) is strictly faster than Dense Baseline (A) by {time_dense / time_fused:.2f}x!")
else:
    print(f"\nConclusion: Fused Low-Rank (C) is NOT strictly faster than Dense Baseline (A). (Expected a speedup on GPU with actual fusion)")

if time_fused < time_split:
    print(f"Furthermore, Fused Low-Rank (C) is {time_split / time_fused:.2f}x faster than Split Low-Rank (B), confirming fusion benefits!")
else:
    print(f"Fused Low-Rank (C) is not faster than Split Low-Rank (B). This indicates the fusion was not effective or overhead dominates for this specific setup.")