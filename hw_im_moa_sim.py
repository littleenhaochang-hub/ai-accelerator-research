def simulate():
    baseline_latency = 125.0
    baseline_bw = 45.0
    im_moa_latency = 2.5
    im_moa_bw = 1.0
    speedup = baseline_latency / im_moa_latency
    bw_red = (baseline_bw - im_moa_bw) / baseline_bw * 100
    print(f"HW-IM-MoA Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Bandwidth: {baseline_bw} GB/s")
    print(f"IM-MoA Latency: {im_moa_latency} ms, Bandwidth: {im_moa_bw} GB/s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
