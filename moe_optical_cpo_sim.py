import time
import math

def simulate_moe_optical_cpo():
    print("Starting MoE Optical Co-Packaged Optics (CPO) DMA Simulation...")
    # Baseline: PCIe Gen 5 x16 (64 GB/s) -> 128 experts, each 100MB = 12.8GB. 
    # Routing 4 experts per token = 400MB.
    pcie_bw_gb_s = 64
    expert_size_mb = 100
    experts_per_token = 4
    
    bytes_to_transfer_mb = expert_size_mb * experts_per_token
    latency_pcie_ms = (bytes_to_transfer_mb / (pcie_bw_gb_s * 1024)) * 1000 + 0.15 # 0.15ms PCIe overhead
    
    # Proposed: Silicon Photonics CPO (Tbps optical interconnect) -> 4 Tbps = 500 GB/s
    optical_bw_gb_s = 500
    latency_optical_ms = (bytes_to_transfer_mb / (optical_bw_gb_s * 1024)) * 1000 + 0.01 # 0.01ms optical routing overhead
    
    speedup = latency_pcie_ms / latency_optical_ms
    
    print(f"Tokens to route: 1, Experts activated: {experts_per_token}")
    print(f"Total payload: {bytes_to_transfer_mb} MB")
    print(f"Baseline PCIe Gen 5 Latency: {latency_pcie_ms:.3f} ms")
    print(f"Proposed Optical CPO Latency: {latency_optical_ms:.3f} ms")
    print(f"Speedup: {speedup:.2f}x")
    
    if speedup > 5.0:
        print("Result: SUCCESS. Optical CPO overcomes the MoE memory wall.")
    else:
        print("Result: FAILED. Insufficient bandwidth improvement.")

if __name__ == '__main__':
    simulate_moe_optical_cpo()
