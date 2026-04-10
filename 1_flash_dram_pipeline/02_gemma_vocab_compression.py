import torch
import math
import time

print("=== Pillar 2: Gemma 256K Vocabulary Compression Simulator ===")
# Gemma 2B configuration
VOCAB_SIZE = 256000
DIM = 2048

# Calculate Baseline
fp16_bytes = VOCAB_SIZE * DIM * 2
print(f"Baseline Gemma Embedding (FP16): {fp16_bytes / (1024**2):.1f} MB")

# To avoid OOM during SVD on the Mac, we evaluate SNR on a representative subset
subset_size = 10000 
print(f"\nGenerating statistical representation of embedding space (subset: {subset_size}x{DIM})...")
# Embeddings typically have zero mean and small variance
E_subset = torch.randn(subset_size, DIM, dtype=torch.float32) * 0.02

def calc_snr(orig, quant):
    mse = torch.mean((orig - quant) ** 2)
    if mse == 0: return float('inf')
    signal = torch.mean(orig ** 2)
    return 10 * torch.log10(signal / mse).item()

# 1. Block-32 INT4 Quantization
print("\n--- Method A: INT4 Block-32 Quantization ---")
block_size = 32
E_reshaped = E_subset.view(-1, block_size)
max_val = torch.max(torch.abs(E_reshaped), dim=-1, keepdim=True)[0].clamp(min=1e-5)
scale = max_val / 7.0
E_q = torch.round(E_reshaped / scale).clamp(-8, 7)
E_dq = (E_q * scale).view(subset_size, DIM)

snr_int4 = calc_snr(E_subset, E_dq)
mem_int4_mb = (VOCAB_SIZE * DIM * 0.5) / (1024**2) # 4 bits = 0.5 bytes
mem_int4_scales = (VOCAB_SIZE * (DIM // block_size) * 2) / (1024**2) # FP16 scales
total_int4_mb = mem_int4_mb + mem_int4_scales
print(f"Footprint: {total_int4_mb:.1f} MB (Weights {mem_int4_mb:.1f}MB + Scales {mem_int4_scales:.1f}MB)")
print(f"SNR: {snr_int4:.2f} dB")

# 2. SVD Low-Rank Decomposition
def evaluate_svd(rank):
    print(f"\n--- Method B: SVD Low-Rank (Rank={rank}) ---")
    U, S, V = torch.svd_lowrank(E_subset, q=rank)
    E_recon = torch.matmul(U, torch.diag(S))
    E_recon = torch.matmul(E_recon, V.t())
    
    snr_svd = calc_snr(E_subset, E_recon)
    # Memory = (Vocab x Rank) + (Rank x Dim) in FP16
    mem_svd_mb = ((VOCAB_SIZE * rank) + (rank * DIM)) * 2 / (1024**2)
    print(f"Footprint: {mem_svd_mb:.1f} MB")
    print(f"SNR: {snr_svd:.2f} dB")

evaluate_svd(128)
evaluate_svd(256)
evaluate_svd(512)

# 3. Hybrid: SVD Rank 512 + INT8 Quantization
print("\n--- Method C: Hybrid SVD (Rank 512) + INT8 ---")
rank = 512
U, S, V = torch.svd_lowrank(E_subset, q=rank)
# Multiply S into U for standard matrix format A = U*S, B = V^T
A = torch.matmul(U, torch.diag(S))
B = V.t()

# Quantize A and B to INT8
A_scale = A.abs().max() / 127
B_scale = B.abs().max() / 127

A_q = torch.round(A / A_scale).clamp(-128, 127)
B_q = torch.round(B / B_scale).clamp(-128, 127)

A_dq = A_q * A_scale
B_dq = B_q * B_scale

E_recon_hybrid = torch.matmul(A_dq, B_dq)
snr_hybrid = calc_snr(E_subset, E_recon_hybrid)

# INT8 size = 1 byte per parameter
mem_hybrid_mb = ((VOCAB_SIZE * rank) + (rank * DIM)) * 1 / (1024**2)
print(f"Footprint: {mem_hybrid_mb:.1f} MB")
print(f"SNR: {snr_hybrid:.2f} dB")

