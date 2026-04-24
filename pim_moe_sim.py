import time
import math

def simulate_pim_moe():
    print("Simulating Processing-in-Memory (PIM) for MoE Experts vs CPU-GPU Memory Transfers...")
    
    # Parameters
    vocab_size = 32000
    d_model = 4096
    num_experts = 8
    expert_size_mb = 128
    
    # Baseline: CPU-GPU Transfer (PCIe Gen4 x16)
    pcie_bandwidth_gb_s = 64
    transfer_time_ms = (expert_size_mb / 1024) / pcie_bandwidth_gb_s * 1000
    compute_time_ms = 2.5
    baseline_total_ms = transfer_time_ms + compute_time_ms
    
    # PIM: Processing inside the DRAM module
    # Transfer time is 0 for weights, only activations are transferred
    activation_size_mb = (d_model * 4) / (1024 * 1024)
    pim_transfer_time_ms = (activation_size_mb / 1024) / pcie_bandwidth_gb_s * 1000
    pim_compute_time_ms = 3.5 # Slightly slower logic in PIM
    pim_total_ms = pim_transfer_time_ms + pim_compute_time_ms
    
    speedup = baseline_total_ms / pim_total_ms
    
    print(f"Baseline (Demand Fetch over PCIe): {baseline_total_ms:.4f} ms per expert")
    print(f"PIM (Processing-in-Memory): {pim_total_ms:.4f} ms per expert")
    print(f"Speedup: {speedup:.2f}x")
    print(f"PIM reduces data movement by {expert_size_mb / activation_size_mb:,.0f}x")

if __name__ == '__main__':
    simulate_pim_moe()
