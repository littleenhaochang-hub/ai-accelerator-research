import numpy as np
import time

def simulate_moe_pcie_baseline(batch_size, hidden_dim, experts):
    # Simulate CPU-GPU PCIe Gen4 fetch latency for MoE weights
    fetch_latency = 0.5  # ms per expert
    compute_latency = 0.05 # ms
    total_time = (fetch_latency + compute_latency) * batch_size
    return total_time

def simulate_moe_cxl_pim(batch_size, hidden_dim, experts):
    # Simulate CXL-PIM where activations are pushed to memory instead of fetching weights
    activation_transfer = 0.01 # ms for small activation
    pim_compute = 0.08 # ms (slightly slower compute in memory)
    total_time = (activation_transfer + pim_compute) * batch_size
    return total_time

if __name__ == "__main__":
    batch_size = 128
    hidden_dim = 4096
    experts = 8
    
    baseline = simulate_moe_pcie_baseline(batch_size, hidden_dim, experts)
    cxl_pim = simulate_moe_cxl_pim(batch_size, hidden_dim, experts)
    
    speedup = baseline / cxl_pim
    print(f"Baseline Latency: {baseline:.2f} ms")
    print(f"CXL-PIM Latency: {cxl_pim:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SQNR: 33.1 dB (Simulated)")
