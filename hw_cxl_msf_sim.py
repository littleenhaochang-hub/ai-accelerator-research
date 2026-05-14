import time
import random

def simulate_pcie_moe_fetch(experts, size_mb):
    start = time.time()
    # Simulate PCIe latency and bandwidth (Gen4 x16 ~ 64GB/s, high latency setup)
    latency = 0.005 # 5ms driver/OS overhead
    transfer = size_mb / 64000.0
    time.sleep(latency + transfer)
    return time.time() - start

def simulate_cxl3_msf_fetch(experts, size_mb):
    start = time.time()
    # Simulate CXL 3.0 Memory Semantics (Sub-microsecond latency, byte-addressable)
    latency = 0.0001 # 100us hardware direct fetch overhead
    transfer = size_mb / 64000.0 # Same bandwidth
    time.sleep(latency + transfer)
    return time.time() - start

if __name__ == "__main__":
    expert_size = 512 # 512MB per expert
    num_requests = 20
    
    pcie_total = sum([simulate_pcie_moe_fetch(1, expert_size) for _ in range(num_requests)])
    cxl_total = sum([simulate_cxl3_msf_fetch(1, expert_size) for _ in range(num_requests)])
    
    print(f"Baseline PCIe MoE Fetch Time: {pcie_total:.4f} s")
    print(f"HW-CXL-MSF MoE Fetch Time: {cxl_total:.4f} s")
    print(f"Speedup: {pcie_total / cxl_total:.2f}x")
