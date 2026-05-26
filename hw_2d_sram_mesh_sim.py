import numpy as np

def simulate_h2d_sram(context_len=262144, head_dim=128):
    # Baseline: External HBM/LPDDR fetching for 256K Context KV Cache
    # Assumes 64 GB/s LPDDR5X bandwidth
    baseline_kv_size_mb = (context_len * head_dim * 2 * 2) / (1024 * 1024)
    baseline_latency_ms = (baseline_kv_size_mb / 64.0) * 1000 + 15.0 # PCIe/Mem Controller overhead
    
    # HW-2D-SRAM: Hardware 2D-Mesh SRAM Fabric
    # Distributes KV cache across a 2D mesh of on-chip SRAM tiles, bypassing DRAM completely
    # Internal mesh bandwidth is assumed to be 8 TB/s
    proposed_latency_ms = (baseline_kv_size_mb / 8192.0) * 1000 + 0.5 # Mesh routing overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline DRAM Fetch Latency (256K): {baseline_latency_ms:.2f} ms")
    print(f"HW-2D-SRAM Mesh Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("DRAM Bandwidth Dependency: 0.0%")

simulate_h2d_sram()
