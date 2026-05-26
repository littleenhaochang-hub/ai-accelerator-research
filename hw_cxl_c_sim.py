import numpy as np

def simulate_hcc_kvc(seq_len=262144, d_model=4096):
    # Baseline: External NVMe swapping for long context
    # Assumes PCIe Gen4 NVMe bandwidth 7 GB/s
    baseline_kv_size_mb = (seq_len * d_model * 2 * 2) / (1024 * 1024)
    baseline_latency_ms = (baseline_kv_size_mb / 7.0) * 1000 + 5.0 # PCIe overhead
    
    # HW-CXL-C: Hardware CXL-Attached Cache with memory tiering
    # Direct memory-semantic access to CXL 3.0 memory (64 GB/s)
    proposed_latency_ms = (baseline_kv_size_mb / 64.0) * 1000 + 1.0 # CXL latency overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline NVMe Swap Latency (256K): {baseline_latency_ms:.2f} ms")
    print(f"HW-CXL-C Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

simulate_hcc_kvc()
