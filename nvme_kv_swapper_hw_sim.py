import time

def software_nvme_kv_swap(memory_size_mb):
    # Simulated CPU overhead + NVMe driver latency for paging out KV blocks
    # Requires OS context switches, filesystem overhead, and CPU DMA setup
    latency = memory_size_mb * 0.8 # ms per MB
    return latency

def hardware_nvme_kv_swap(memory_size_mb):
    # Simulated Hardware NVMe Controller (Direct P2P DMA from SRAM to NVMe)
    # Bypasses CPU and OS completely, directly addressing NVMe LBA
    latency = memory_size_mb * 0.05 # ms per MB
    return latency

def main():
    memory_size_mb = 4096 # 4GB of cold KV cache to swap
    
    print("Running Hardware NVMe KV Cache Swapper Simulation...")
    sw_lat = software_nvme_kv_swap(memory_size_mb)
    print(f"Software NVMe Swap Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_nvme_kv_swap(memory_size_mb)
    print(f"Hardware NVMe Swap Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
