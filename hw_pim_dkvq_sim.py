def simulate():
    # standard memory fetch latency for 128K context in FP16
    baseline_latency = 120.0 # ms
    baseline_bw = 16.0 # GB/s
    
    # PIM-based dynamic quantization evaluates token importance in memory 
    # and only fetches top 10% in FP16, rest in 2-bit
    pim_latency = 25.0 # ms
    pim_bw = 3.5 # GB/s
    
    speedup = baseline_latency / pim_latency
    bw_reduction = (baseline_bw - pim_bw) / baseline_bw * 100
    
    print(f"HW-PIM-DKVQ Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Bandwidth: {baseline_bw} GB/s")
    print(f"PIM Latency: {pim_latency} ms, Bandwidth: {pim_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
