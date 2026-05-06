import time
import random

def simulate_moe_bottleneck():
    num_tokens = 1024
    expert_size_mb = 128
    
    # Baseline: CPU-GPU DMA Fetching (PCIe Gen4)
    # Transferring 128MB per token (worst case, batch 1)
    pcie_bw_gbps = 64
    time_dma = (expert_size_mb / 1024) / pcie_bw_gbps * num_tokens
    
    # Proposed: HW-MAP (Hardware MoE Activation Pushing to CXL/PIM)
    # Transferring 2KB token activation instead of 128MB weight
    token_size_kb = 2
    cxl_bw_gbps = 32
    time_map_transfer = (token_size_kb / (1024*1024)) / cxl_bw_gbps * num_tokens
    pim_compute_time = 0.001 * num_tokens # 1ms per token
    time_map = time_map_transfer + pim_compute_time
    
    print("=== HW-MAP PIM MoE Simulation ===")
    print(f"Baseline (PCIe Weight Fetch) Latency: {time_dma:.4f} s")
    print(f"HW-MAP (Activation Push) Latency: {time_map:.4f} s")
    speedup = time_dma / time_map
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {(expert_size_mb * 1024) / token_size_kb:.2f}x")

if __name__ == '__main__':
    simulate_moe_bottleneck()
