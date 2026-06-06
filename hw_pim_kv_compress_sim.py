def simulate():
    baseline_latency = 95.0
    baseline_bw = 32.0
    hw_pim_latency = 10.5
    hw_pim_bw = 4.0
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-KV-Compress Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
