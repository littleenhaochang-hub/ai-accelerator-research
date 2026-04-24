import time

def software_kv_defrag(memory_size_mb):
    # Simulated CPU/GPU software defragmentation of KV Cache
    # Requires pausing token execution, locking memory, copying blocks
    latency = memory_size_mb * 0.5 # ms per MB
    return latency

def hardware_bg_defrag(memory_size_mb):
    # Simulated Hardware Background Defragmentation Engine
    # Runs parallel to execution via DMA, stalling MACs minimally
    latency = memory_size_mb * 0.01 # ms per MB effective stall
    return latency

def main():
    memory_size_mb = 1024 # 1GB fragmented KV cache
    
    print("Running Hardware KV Cache Defragmenter Simulation...")
    sw_lat = software_kv_defrag(memory_size_mb)
    print(f"Software Defrag Stall Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_bg_defrag(memory_size_mb)
    print(f"Hardware Defrag Stall Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup (Reduction in Stalls): {speedup:.2f}x")

if __name__ == '__main__':
    main()
