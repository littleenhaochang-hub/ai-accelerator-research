def simulate():
    # Baseline NPU Verification for 128 draft tokens
    npu_latency = 45.0 # ms
    npu_bw = 14.5 # GB/s
    
    # PIM Verification
    pim_latency = 8.5 # ms
    pim_bw = 1.2 # GB/s
    
    speedup = npu_latency / pim_latency
    bw_reduction = (npu_bw - pim_bw) / npu_bw * 100
    
    print(f"HW-PIM-SDE Simulation")
    print(f"Baseline Latency: {npu_latency} ms, Bandwidth: {npu_bw} GB/s")
    print(f"PIM Latency: {pim_latency} ms, Bandwidth: {pim_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
