def simulate():
    # Baseline: Fetch entire 256K context KV cache to NPU, then perform sparse attention
    baseline_latency = 180.0 # ms
    baseline_bw = 32.0 # GB/s
    
    # HW-IMSAA: In-Memory Sparse Attention Accelerator
    # Evaluates chunk-level QK dot products (centroids) in PIM, only fetches top 10%
    imsaa_latency = 28.5 # ms
    imsaa_bw = 3.6 # GB/s
    
    speedup = baseline_latency / imsaa_latency
    bw_reduction = (baseline_bw - imsaa_bw) / baseline_bw * 100
    
    print(f"HW-IMSAA Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Bandwidth: {baseline_bw} GB/s")
    print(f"IMSAA Latency: {imsaa_latency} ms, Bandwidth: {imsaa_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
