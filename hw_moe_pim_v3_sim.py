import math
import time
import random

def simulate_baseline_moe_fetch(num_tokens, num_experts, expert_size_mb, bandwidth_gb_s):
    # Baseline: CPU-GPU PCIe Gen4 transfer
    total_time = 0
    bandwidth_mb_ms = bandwidth_gb_s * 1024 / 1000
    for _ in range(num_tokens):
        fetch_time = expert_size_mb / bandwidth_mb_ms
        total_time += fetch_time
    return total_time

def simulate_moe_pim_v3(num_tokens, num_experts, expert_size_mb, bandwidth_gb_s):
    # HW-MoE-PIM-v3: Process-in-Memory CXL 3.1
    total_time = 0
    # Data sent to memory is only the activation (very small compared to weights)
    activation_size_mb = 0.05 # 50 KB
    bandwidth_mb_ms_cxl = (64) * 1024 / 1000 # CXL 3.1 bandwidth 64 GB/s
    
    for _ in range(num_tokens):
        fetch_time = activation_size_mb / bandwidth_mb_ms_cxl
        # Add PIM compute latency overhead
        fetch_time += 0.002
        total_time += fetch_time
    return total_time

if __name__ == "__main__":
    num_tokens = 4096
    num_experts = 128
    expert_size_mb = 100 # INT4 quantized expert
    bandwidth_gb_s = 16 # PCIe Gen4 x8 equivalent
    
    baseline_time = simulate_baseline_moe_fetch(num_tokens, num_experts, expert_size_mb, bandwidth_gb_s)
    pim_v3_time = simulate_moe_pim_v3(num_tokens, num_experts, expert_size_mb, bandwidth_gb_s)
    
    speedup = baseline_time / pim_v3_time
    bandwidth_reduction = expert_size_mb / 0.05
    
    print(f"Baseline Time: {baseline_time:.2f} ms")
    print(f"HW-MoE-PIM-v3 Time: {pim_v3_time:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bandwidth_reduction:.2f}x")
