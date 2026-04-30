import math

def simulate_software_sparse_attention(seq_len, sparsity_ratio):
    # O(N log N) or O(N * C) overhead for clustering / LSH software routing
    overhead_ms = (seq_len * math.log2(seq_len)) * 0.005
    compute_ms = (seq_len * seq_len * (1 - sparsity_ratio)) * 0.0001
    return overhead_ms + compute_ms

def simulate_hardware_osahr(seq_len, sparsity_ratio):
    # O(1) per token routing via In-SRAM Hash Routing (OSAHR)
    overhead_ms = seq_len * 0.0002
    compute_ms = (seq_len * seq_len * (1 - sparsity_ratio)) * 0.0001
    return overhead_ms + compute_ms

seq_len = 32768
sparsity_ratio = 0.90

soft_latency = simulate_software_sparse_attention(seq_len, sparsity_ratio)
hard_latency = simulate_hardware_osahr(seq_len, sparsity_ratio)

speedup = soft_latency / hard_latency

print(f"Software Sparse Attention Latency: {soft_latency:.2f} ms")
print(f"Hardware OSAHR Latency: {hard_latency:.2f} ms")
print(f"Throughput Speedup: {speedup:.2f}x")
