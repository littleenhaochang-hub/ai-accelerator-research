import time
import math

def simulate_moe_cxl_pim(num_experts=256, expert_size_mb=128, batch_size=1, hidden_dim=4096):
    print(f"Simulating CXL-PIM MoE Expert Fetching...")
    print(f"Config: {num_experts} Experts, {expert_size_mb}MB each, Hidden Dim: {hidden_dim}")
    
    # Simulate standard PCIe 4.0 DMA fetching (Baseline)
    pcie_bandwidth_gb_s = 32.0 # GB/s
    pcie_latency_us = 5.0
    
    # Simulate CXL 3.0 PIM (Processing in Memory)
    cxl_bandwidth_gb_s = 64.0
    cxl_latency_us = 1.0
    
    # Payload
    transfer_bytes = expert_size_mb * 1024 * 1024
    
    # Baseline timing
    baseline_time_ms = (transfer_bytes / (pcie_bandwidth_gb_s * 1024**3)) * 1000 + (pcie_latency_us / 1000.0)
    
    # CXL-PIM timing (PIM executes locally, only sending the activation vector and retrieving result)
    activation_bytes = batch_size * hidden_dim * 2 # FP16
    cxl_time_ms = (activation_bytes / (cxl_bandwidth_gb_s * 1024**3)) * 1000 + (cxl_latency_us / 1000.0)
    
    speedup = baseline_time_ms / cxl_time_ms
    bandwidth_reduction = transfer_bytes / activation_bytes
    
    print(f"Baseline PCIe Gen4 Transfer Time: {baseline_time_ms:.4f} ms")
    print(f"CXL-PIM Transfer Time: {cxl_time_ms:.4f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bandwidth_reduction:.2f}x")
    
    return speedup, bandwidth_reduction

if __name__ == "__main__":
    simulate_moe_cxl_pim()
