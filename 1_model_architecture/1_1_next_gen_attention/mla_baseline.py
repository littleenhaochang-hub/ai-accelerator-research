import torch
import torch.nn as nn
import torch.nn.functional as F

print("=====================================================")
print(" Multi-Head Latent Attention (MLA) Baseline (DeepSeek-V3)")
print(" Goal: Simulate the extreme KV Cache compression of MLA vs standard MHA.")
print("       Measure FLOPs and Memory footprint during generation.")
print("=====================================================\n")

# 1. Architecture Parameters (Scaled down for simulation)
BATCH_SIZE = 1
SEQ_LEN = 4096
D_MODEL = 2048       # Hidden dimension
N_HEADS = 16         # Number of attention heads
D_HEAD = 128         # Dimension per head
D_KV_COMPRESSED = 512 # The Latent Vector dimension (Crucial for MLA)

print(f"Simulating Attention: B={BATCH_SIZE}, SeqLen={SEQ_LEN}, d_model={D_MODEL}")

# Generate Random Input States (e.g., Output from an MLP block)
hidden_states = torch.randn(BATCH_SIZE, SEQ_LEN, D_MODEL)

# ---------------------------------------------------------
# Scenario A: Standard Multi-Head Attention (MHA)
# ---------------------------------------------------------
# MHA stores explicit K and V for every head and every token
W_q = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False)
W_k = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False)
W_v = nn.Linear(D_MODEL, N_HEADS * D_HEAD, bias=False)
W_o = nn.Linear(N_HEADS * D_HEAD, D_MODEL, bias=False)

# Compute MHA Projections
q_mha = W_q(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
k_mha = W_k(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
v_mha = W_v(hidden_states).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)

# MHA Memory Footprint (KV Cache)
# Need to store (K, V) for all heads
mha_kv_cache_size = k_mha.numel() * 2 + v_mha.numel() * 2 # FP16 = 2 bytes
print(f"Standard MHA KV Cache Size (FP16): {mha_kv_cache_size / 1024 / 1024:.2f} MB")

# Calculate MHA Attention (O(N^2))
attn_scores_mha = torch.matmul(q_mha, k_mha.transpose(-2, -1)) / (D_HEAD ** 0.5)
attn_probs_mha = F.softmax(attn_scores_mha, dim=-1)
mha_output = torch.matmul(attn_probs_mha, v_mha)

# ---------------------------------------------------------
# Scenario B: Multi-Head Latent Attention (MLA)
# ---------------------------------------------------------
# MLA compresses the huge KV state into a tiny latent vector (c_kv).
# It does NOT store K and V for every head. It only stores c_kv.

# Compression Projection (Down-proj)
W_down_kv = nn.Linear(D_MODEL, D_KV_COMPRESSED, bias=False)

# Expansion Projections (Up-proj)
W_up_k = nn.Linear(D_KV_COMPRESSED, N_HEADS * D_HEAD, bias=False)
W_up_v = nn.Linear(D_KV_COMPRESSED, N_HEADS * D_HEAD, bias=False)

# 1. Compress into Latent Vector (This is what is actually cached!)
c_kv = W_down_kv(hidden_states)

# MLA Memory Footprint (KV Cache)
mla_kv_cache_size = c_kv.numel() * 2 # Storing only c_kv in FP16
print(f"DeepSeek MLA KV Cache Size (FP16): {mla_kv_cache_size / 1024 / 1024:.2f} MB")
print(f"Memory Reduction: {mha_kv_cache_size / mla_kv_cache_size:.1f}x smaller")

# 2. Decompress during Inference
# When attention is computed, c_kv is expanded back into full K and V
k_mla = W_up_k(c_kv).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)
v_mla = W_up_v(c_kv).view(BATCH_SIZE, SEQ_LEN, N_HEADS, D_HEAD).transpose(1, 2)

# Calculate MLA Attention
attn_scores_mla = torch.matmul(q_mha, k_mla.transpose(-2, -1)) / (D_HEAD ** 0.5)
attn_probs_mla = F.softmax(attn_scores_mla, dim=-1)
mla_output = torch.matmul(attn_probs_mla, v_mha) # Note: v_mha is used here simply to output a tensor, the core metric is memory

print("\n--- Conclusion ---")
print("MLA dramatically shrinks the memory bandwidth bottleneck for Edge GPUs.")
print("However, expanding c_kv into full K and V during the forward pass requires massive O(N^2) FLOPs on the Up-Projection matrices.")
print("Hardware Architect Challenge: How do we optimize the Up-Projection so it doesn't throttle the ALU while saving memory?")
