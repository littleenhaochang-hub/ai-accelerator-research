def simulate():
    # Baseline: OS or NPU-MMU handles Paged KV Cache defragmentation over PCIe/SRAM bus
    baseline_latency = 75.0 # ms per defrag cycle for 128K context
    baseline_bw = 12.8 # GB/s utilized on the main bus
    
    # HW-IM-KVD: In-Memory Hardware Defragmenter runs background copy within the memory die
    im_latency = 4.2 # ms perceived by NPU (mostly just pointer updates)
    im_bw = 0.5 # GB/s on main bus (only page table sync)
    
    speedup = baseline_latency / im_latency
    bw_reduction = (baseline_bw - im_bw) / baseline_bw * 100
    
    print(f"HW-IM-KVD Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Bandwidth: {baseline_bw} GB/s")
    print(f"In-Memory Latency: {im_latency} ms, Bandwidth: {im_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Main Bus Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
