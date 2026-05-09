import time
import random

def simulate_moe_decoding(seq_len=1024, use_cxl_prefetch=False):
    print(f"Starting MoE Decoding Simulation (seq_len={seq_len}, CXL_Prefetch={use_cxl_prefetch})...")
    
    compute_time = 0.5  # ms per token
    base_pcie_latency = 2.0  # ms per token
    cxl_prefetch_latency = 0.1  # ms overhead with CXL 3.0 speculative prefetch
    
    total_time = 0.0
    for i in range(seq_len):
        if use_cxl_prefetch:
            total_time += max(compute_time, cxl_prefetch_latency)
        else:
            total_time += compute_time + base_pcie_latency
            
    return total_time

if __name__ == "__main__":
    baseline_time = simulate_moe_decoding(seq_len=1024, use_cxl_prefetch=False)
    cxl_time = simulate_moe_decoding(seq_len=1024, use_cxl_prefetch=True)
    
    speedup = baseline_time / cxl_time
    
    print("\n--- Simulation Results ---")
    print(f"Baseline Latency (PCIe Gen4): {baseline_time:.2f} ms")
    print(f"CXL 3.0 Prefetch Latency: {cxl_time:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Metric: {speedup:.2f}x throughput speedup by overlapping memory fetch latency with compute.")
