import time
import numpy as np

def simulate_standard_moe_fetch(expert_size_mb=128, num_tokens=1000, pcie_bandwidth_gbps=32):
    # Standard: CPU fetches, sends over PCIe, stalls GPU
    print("Simulating Standard MoE Fetching...")
    total_latency = 0
    start = time.time()
    for _ in range(num_tokens):
        fetch_time = expert_size_mb / (pcie_bandwidth_gbps * 1024)
        compute_time = 0.001 # 1ms compute
        total_latency += fetch_time + compute_time
    end = time.time()
    return total_latency

def simulate_hamp_moe_prefetch(expert_size_mb=128, num_tokens=1000, pcie_bandwidth_gbps=32):
    # HAMP: Hardware Asynchronous DMA overlaps fetch with compute
    print("Simulating Hardware Asynchronous MoE Prefetching (HAMP)...")
    total_latency = 0
    fetch_time = expert_size_mb / (pcie_bandwidth_gbps * 1024)
    compute_time = 0.001
    
    start = time.time()
    # First fetch cannot be overlapped
    total_latency += fetch_time + compute_time
    
    for _ in range(1, num_tokens):
        # Hardware overlaps fetch and compute. Max of the two determines the bottleneck for the pipeline stage.
        total_latency += max(fetch_time, compute_time)
        
    end = time.time()
    return total_latency

if __name__ == "__main__":
    baseline = simulate_standard_moe_fetch()
    hamp = simulate_hamp_moe_prefetch()
    speedup = baseline / hamp
    print(f"Baseline Latency: {baseline:.4f} s")
    print(f"HAMP Latency: {hamp:.4f} s")
    print(f"Speedup: {speedup:.2f}x")
