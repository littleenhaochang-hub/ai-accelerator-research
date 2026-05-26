import math

def simulate_skcp():
    # Baseline: Fetching full K-Cache for long context (128K)
    num_tokens = 128 * 1024
    dim = 4096
    k_cache_size_mb = (num_tokens * dim * 2) / (1024 * 1024)
    bandwidth_gb_s = 100
    baseline_latency_ms = (k_cache_size_mb / bandwidth_gb_s) * 1000

    # Proposed: Hardware Sparse K-Cache Predictor (HW-SKCP)
    # Predicts which K-Cache blocks are needed before fetching from DRAM
    sparsity = 0.90
    overhead_latency_ms = 0.5
    proposed_latency_ms = ((k_cache_size_mb * (1 - sparsity)) / bandwidth_gb_s) * 1000 + overhead_latency_ms

    speedup = baseline_latency_ms / proposed_latency_ms
    print(f"Simulation Complete: HW-SKCP (Hardware Sparse K-Cache Predictor)")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_skcp()