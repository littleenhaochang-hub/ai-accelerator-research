import torch
import torch.nn as nn
import torch.nn.functional as F
import time

print("=====================================================")
print(" Multi-Head Latent Attention (MLA) Baseline (DeepSeek-V3)")
print(" Goal: Simulate the extreme KV Cache compression of MLA vs standard MHA.")
print("       Measure FLOPs and Memory footprint during generation.")
print("=====================================================\n")

# Determine if CUDA is available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}\n")

# 1. Architecture Parameters (Scaled down for simulation)
BATCH_SIZE = 1
SEQ_LEN = 4096
D_MODEL = 2048       # Hidden dimension
N_HEADS = 16         # Number of attention heads
D_HEAD = 128         # Dimension per head
D_KV_COMPRESSED = 512 # The Latent Vector dimension (Crucial for MLA)
LOW_RANK_DIM = 128   # R: The low-rank dimension for factorization (R << D_KV_COMPRESSED, N_HEADS * D_HEAD)

print(f"Simulating Attention: B={BATCH_SIZE}, SeqLen={SEQ_LEN}, d_model={D_MODEL}")
print(f"MLA Parameters: D_KV_COMPRESSED={D_KV_COMPRESSED}, LOW_RANK_DIM={LOW_RANK_DIM}")

# Generate Random Input States (e.g., Output from an MLP block)
hidden_states = torch.randn(BATCH_SIZE, SEQ_LEN, D_MODEL).to(device)

# ---------------------------------------------------------
# Scenario A: Standard Multi-Head Attention (MHA)
# ---------------------------------------------------------
# MHA stores explicit K and V for every head and every token
W_q = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False).to(device)
W_k = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False).to(device)
W_v = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False).to(device)
W_o = nn.Linear(N_HEADS * D_HEAD, D_MODEL, bias=False).to(device)

# Compute MHA Projections
q_mha = W_q(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
k_mha = W_k(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
v_mha = W_v(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)

# MHA Memory Footprint (KV Cache)
# Need to store (K, V) for all heads
mha_kv_cache_size = k_mha.numel() * k_mha.element_size() + v_mha.numel() * v_mha.element_size() # Actual bytes
print(f"Standard MHA KV Cache Size: {mha_kv_cache_size / 1024 / 1024:.2f} MB")

# Calculate MHA Attention (O(N^2))
# (This part is not the focus of the optimization, but included for completeness)
attn_scores_mha = torch.matmul(q_mha, k_mha.transpose(-2, -1)) / (D_HEAD ** 0.5)
attn_probs_mha = F.softmax(attn_scores_mha, dim=-1)
mha_output = torch.matmul(attn_probs_mha, v_mha)

# ---------------------------------------------------------
# Scenario B: Multi-Head Latent Attention (MLA)
# ---------------------------------------------------------
# MLA compresses the huge KV state into a tiny latent vector (c_kv).
# It does NOT store K and V for every head. It only stores c_kv.

# Compression Projection (Down-proj)
W_down_kv = nn.Linear(D_MODEL, D_KV_COMPRESSED, bias=False).to(device)

# Expansion Projections (Up-proj)
W_up_k = nn.Linear(D_KV_COMPRESSED, N_HEADS * D_HEAD, bias=False).to(device)
W_up_v = nn.Linear(D_KV_COMPRESSED, N_HEADS * D_HEAD, bias=False).to(device)

# 1. Compress into Latent Vector (This is what is actually cached!)
c_kv = W_down_kv(hidden_states)

# MLA Memory Footprint (KV Cache)
mla_kv_cache_size = c_kv.numel() * c_kv.element_size() # Storing only c_kv in actual bytes
print(f"\nDeepSeek MLA KV Cache Size: {mla_kv_cache_size / 1024 / 1024:.2f} MB")
print(f"Memory Reduction: {mha_kv_cache_size / mla_kv_cache_size:.1f}x smaller")

# 2. Decompress during Inference (Baseline MLA)
print("\n--- Baseline MLA Up-Projection Performance ---")
if device.type == 'cuda':
    torch.cuda.synchronize()
start_time_mla = time.perf_counter()
k_mla = W_up_k(c_kv).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
v_mla = W_up_v(c_kv).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
if device.type == 'cuda':
    torch.cuda.synchronize()
end_time_mla = time.perf_counter()
latency_mla = (end_time_mla - start_time_mla) * 1000

# Calculate FLOPs for baseline up-projections
# For W_up_k: c_kv @ W_up_k^T. Shape (B, S, D_KV_COMPRESSED) @ (D_KV_COMPRESSED, N_HEADS*D_HEAD)
flops_up_k_mla = BATCH_SIZE * SEQ_LEN * D_KV_COMPRESSED * (N_HEADS * D_HEAD) * 2 # M*N*K * 2 for matmul
flops_up_v_mla = BATCH_SIZE * SEQ_LEN * D_KV_COMPRESSED * (N_HEADS * D_HEAD) * 2
total_flops_mla = flops_up_k_mla + flops_up_v_mla
print(f"Baseline MLA Up-Projection FLOPs: {total_flops_mla / 1e9:.2f} GFLOPs")
print(f"Baseline MLA Up-Projection Latency: {latency_mla:.3f} ms")

# Calculate MLA Attention (using original Q, but MLA K/V for consistency)
attn_scores_mla = torch.matmul(q_mha, k_mla.transpose(-2, -1)) / (D_HEAD ** 0.5)
attn_probs_mla = F.softmax(attn_scores_mla, dim=-1)
mla_output = torch.matmul(attn_probs_mla, v_mla)


# ---------------------------------------------------------
# Scenario C: Multi-Head Latent Attention (MLA) with Low-Rank Factorization
# ---------------------------------------------------------
print("\n--- Low-Rank Factorized MLA Up-Projection Performance ---")

# Apply low-rank factorization to W_up_k and W_up_v
# Original: W_up_X (D_KV_COMPRESSED, N_HEADS * D_HEAD)
# Decomposed: M_X1 (D_KV_COMPRESSED, R), M_X2 (R, N_HEADS * D_HEAD)

# M_k1, M_v1 are the first factors (from D_KV_COMPRESSED to R)
M_k1 = nn.Linear(D_KV_COMPRESSED, LOW_RANK_DIM, bias=False).to(device)
M_v1 = nn.Linear(D_KV_COMPRESSED, LOW_RANK_DIM, bias=False).to(device)

# M_k2, M_v2 are the second factors (from R to N_HEADS * D_HEAD)
M_k2 = nn.Linear(LOW_RANK_DIM, N_HEADS * D_HEAD, bias=False).to(device)
M_v2 = nn.Linear(LOW_RANK_DIM, N_HEADS * D_HEAD, bias=False).to(device)

# Memory footprint of the low-rank up-projection weights
# Original: W_up_k + W_up_v = 2 * D_KV_COMPRESSED * (N_HEADS * D_HEAD)
original_up_weight_memory = 2 * (D_KV_COMPRESSED * N_HEADS * D_HEAD * W_up_k.weight.element_size())

# Factorized: M_k1 + M_k2 + M_v1 + M_v2 = 2 * (D_KV_COMPRESSED * R + R * N_HEADS * D_HEAD)
factorized_up_weight_memory = 2 * (D_KV_COMPRESSED * LOW_RANK_DIM + LOW_RANK_DIM * N_HEADS * D_HEAD) * M_k1.weight.element_size()

print(f"Original Up-Projection Weights Memory: {original_up_weight_memory / 1024:.2f} KB")
print(f"Factorized Up-Projection Weights Memory: {factorized_up_weight_memory / 1024:.2f} KB")
print(f"Weight Memory Reduction: {original_up_weight_memory / factorized_up_weight_memory:.1f}x smaller")

# 2. Decompress during Inference with Low-Rank Factorization
if device.type == 'cuda':
    torch.cuda.synchronize()
start_time_low_rank = time.perf_counter()
# k_factorized = c_kv @ M_k1^T @ M_k2^T
temp_k = M_k1(c_kv) # (B, S, D_KV_COMPRESSED) @ (D_KV_COMPRESSED, R) -> (B, S, R)
k_low_rank = M_k2(temp_k).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)

# v_factorized = c_kv @ M_v1^T @ M_v2^T
temp_v = M_v1(c_kv) # (B, S, D_KV_COMPRESSED) @ (D_KV_COMPRESSED, R) -> (B, S, R)
v_low_rank = M_v2(temp_v).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
if device.type == 'cuda':
    torch.cuda.synchronize()
end_time_low_rank = time.perf_counter()
latency_low_rank = (end_time_low_rank - start_time_low_rank) * 1000

# Calculate FLOPs for factorized up-projections
# For k_low_rank:
#   temp_k = c_kv @ M_k1^T : (B, S, D_KV_COMPRESSED) @ (D_KV_COMPRESSED, R) -> (B, S, R)
flops_temp_k = BATCH_SIZE * SEQ_LEN * D_KV_COMPRESSED * LOW_RANK_DIM * 2
#   k_low_rank = temp_k @ M_k2^T : (B, S, R) @ (R, N_HEADS*D_HEAD) -> (B, S, N_HEADS*D_HEAD)
flops_k_low_rank = BATCH_SIZE * SEQ_LEN * LOW_RANK_DIM * (N_HEADS * D_HEAD) * 2

# Total for K and V
total_flops_low_rank = 2 * (flops_temp_k + flops_k_low_rank)
print(f"Factorized MLA Up-Projection FLOPs: {total_flops_low_rank / 1e9:.2f} GFLOPs")
print(f"Factorized MLA Up-Projection Latency: {latency_low_rank:.3f} ms")

print(f"FLOPs Reduction: {total_flops_mla / total_flops_low_rank:.1f}x smaller")
print(f"Latency Improvement: {latency_mla / latency_low_rank:.1f}x faster")


# Optional: Verify output shapes match
assert k_mla.shape == k_low_rank.shape
assert v_mla.shape == v_low_rank.shape
print(f"\nUp-projected K/V shape: {k_low_rank.shape} (Matches baseline)")

print("\n--- Conclusion ---")
print("MLA dramatically shrinks the memory bandwidth bottleneck for Edge GPUs.")
print("The proposed Low-Rank Factorization for Up-Projection matrices significantly reduces:")
print(f"  1. Compute FLOPs for up-projection from {total_flops_mla / 1e9:.2f} GFLOPs to {total_flops_low_rank / 1e9:.2f} GFLOPs ({total_flops_mla / total_flops_low_rank:.1f}x reduction).")
print(f"  2. Inference Latency for up-projection from {latency_mla:.3f} ms to {latency_low_rank:.3f} ms ({latency_mla / latency_low_rank:.1f}x speedup).")
print(f"  3. Memory footprint of the Up-Projection weights from {original_up_weight_memory / 1024:.2f} KB to {factorized_up_weight_memory / 1024:.2f} KB ({original_up_weight_memory / factorized_up_weight_memory:.1f}x reduction).")
print("This approach helps mitigate the ALU throttling issue identified in MLA, making it more compute-efficient while retaining its memory-saving benefits.")