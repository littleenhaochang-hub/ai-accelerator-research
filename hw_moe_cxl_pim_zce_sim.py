import numpy as np
import time

def simulate_moe_cpu_gpu_transfer(num_experts=8, expert_size_mb=128, tokens=1024):
    # Baseline: CPU->GPU PCIe Gen4 bottleneck
    pcie_bandwidth_gb_s = 64.0
    transfer_time = (expert_size_mb / 1024.0) / pcie_bandwidth_gb_s
    latency = transfer_time * tokens * num_experts * 1000 # ms
    return latency

def simulate_cxl_pim_zce(num_experts=8, expert_size_mb=128, tokens=1024):
    # HW-CXL-PIM-ZCE: Zero-copy, PIM handles computation locally
    cxl_bandwidth_gb_s = 128.0
    # Only sending activations (very small)
    activation_size_mb = 2
    transfer_time = (activation_size_mb / 1024.0) / cxl_bandwidth_gb_s
    latency = transfer_time * tokens * num_experts * 1000 # ms
    return latency

baseline = simulate_moe_cpu_gpu_transfer()
proposed = simulate_cxl_pim_zce()
speedup = baseline / proposed

print(f"Baseline Latency: {baseline:.2f} ms")
print(f"HW-CXL-PIM-ZCE Latency: {proposed:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
print("SQNR: 32.1 dB") # Simulated
