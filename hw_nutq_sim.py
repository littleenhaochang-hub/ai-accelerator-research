import math

def simulate_nutq():
    # Baseline: Uniform INT4 KV Cache
    seq_len = 32 * 1024 # 32K context
    dim = 4096
    baseline_bits_per_element = 4
    baseline_memory_mb = (seq_len * dim * 2 * baseline_bits_per_element) / (8 * 1024 * 1024)
    bandwidth_gb_s = 100
    baseline_latency_ms = (baseline_memory_mb / bandwidth_gb_s) * 1000

    # Proposed: HW-NUTQ (Hardware Non-Uniform Token Quantizer)
    # Important tokens (5%) get 8-bit, normal tokens (15%) get 4-bit, background (80%) get 1.58-bit (ternary)
    avg_bits_per_element = 0.05 * 8 + 0.15 * 4 + 0.80 * 1.58
    proposed_memory_mb = (seq_len * dim * 2 * avg_bits_per_element) / (8 * 1024 * 1024)
    overhead_ms = 0.25 # hardware predictor overhead
    proposed_latency_ms = (proposed_memory_mb / bandwidth_gb_s) * 1000 + overhead_ms

    speedup = baseline_latency_ms / proposed_latency_ms
    memory_reduction = (baseline_memory_mb - proposed_memory_mb) / baseline_memory_mb * 100

    print(f"Simulation Complete: HW-NUTQ (Hardware Non-Uniform Token Quantizer)")
    print(f"Baseline Latency (INT4): {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency (NUTQ): {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Memory Footprint Reduction: {memory_reduction:.2f}%")

if __name__ == '__main__':
    simulate_nutq()