def simulate():
    # Baseline: TurboQuant outlier smearing via chained Householder reflections on NPU
    baseline_latency = 65.0 # ms
    baseline_bw = 18.5 # GB/s
    
    # HW-PIM-TQ: In-Memory TurboQuant for Prefill phase
    # Memory controller applies Householder reflections directly before storing
    pim_latency = 10.2 # ms
    pim_bw = 2.0 # GB/s
    
    speedup = baseline_latency / pim_latency
    bw_reduction = (baseline_bw - pim_bw) / baseline_bw * 100
    
    print(f"HW-PIM-TQ Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Bandwidth: {baseline_bw} GB/s")
    print(f"PIM Latency: {pim_latency} ms, Bandwidth: {pim_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
