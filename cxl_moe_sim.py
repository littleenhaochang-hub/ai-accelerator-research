import time

def simulate_cxl_moe():
    print("Simulating CXL 3.0 Memory Pooling vs PCIe Gen4 for MoE Expert Fetching...")
    
    expert_size_mb = 128
    
    # PCIe Gen 4 x16 Baseline
    pcie_bw_gbs = 64
    pcie_latency_ns = 1500  # PCIe protocol overhead
    pcie_transfer_ms = (expert_size_mb / pcie_bw_gbs) + (pcie_latency_ns / 1_000_000)
    
    # CXL 3.0
    cxl_bw_gbs = 64 # Same bandwidth, but memory-semantic
    cxl_latency_ns = 200 # Flit-level memory semantic latency
    cxl_transfer_ms = (expert_size_mb / cxl_bw_gbs) + (cxl_latency_ns / 1_000_000)
    
    # Context Switching / OS overhead
    pcie_os_overhead_ms = 1.5 # DMA setup
    cxl_os_overhead_ms = 0.05 # Direct memory load via load/store instructions
    
    total_pcie_ms = pcie_transfer_ms + pcie_os_overhead_ms
    total_cxl_ms = cxl_transfer_ms + cxl_os_overhead_ms
    
    speedup = total_pcie_ms / total_cxl_ms
    
    print(f"PCIe Gen4 Total Fetch Time: {total_pcie_ms:.4f} ms")
    print(f"CXL 3.0 Total Fetch Time:   {total_cxl_ms:.4f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("Conclusion: CXL 3.0 eliminates OS/DMA overhead, enabling memory-semantic byte-addressable expert loads.")

if __name__ == '__main__':
    simulate_cxl_moe()
