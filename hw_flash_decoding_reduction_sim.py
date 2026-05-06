import time
import numpy as np

def simulate_software_flash_decoding_reduction(num_kv_blocks=1024, head_dim=128):
    # Software flash decoding: multiple SMs compute partial softmax, then a final reduction is done in HBM/L2
    print(f"Simulating Software Flash-Decoding Reduction (Blocks: {num_kv_blocks})...")
    # Simulate memory read/write latency for partial sums
    partial_sum_memory_mb = (num_kv_blocks * head_dim * 4) / (1024**2) # 4 bytes for FP32
    latency = num_kv_blocks * 0.00005 # Memory bound reduction
    return partial_sum_memory_mb, latency

def simulate_hardware_reduction_tree(num_kv_blocks=1024, head_dim=128):
    # HW-FDRT: On-chip hardware reduction tree (adder tree) aggregates partial sums on the fly
    print(f"Simulating Hardware Flash-Decoding Reduction Tree (HW-FDRT)...")
    partial_sum_memory_mb = 0 # No need to write to DRAM/L2, reduced in register/SRAM stream
    latency = np.log2(num_kv_blocks) * 0.00001 # O(log N) tree latency, fully compute bound
    return partial_sum_memory_mb, latency

if __name__ == "__main__":
    sw_mem, sw_lat = simulate_software_flash_decoding_reduction()
    hw_mem, hw_lat = simulate_hardware_reduction_tree()
    
    print(f"Software Reduction Latency: {sw_lat:.5f} s, DRAM overhead: {sw_mem:.4f} MB")
    print(f"HW-FDRT Latency: {hw_lat:.5f} s, DRAM overhead: {hw_mem:.4f} MB")
    print(f"Latency Speedup: {sw_lat/hw_lat:.2f}x")
