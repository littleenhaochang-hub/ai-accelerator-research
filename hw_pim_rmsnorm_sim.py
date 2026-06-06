def simulate():
    baseline_latency = 30.0
    baseline_bw = 10.0
    hw_pim_latency = 4.5
    hw_pim_bw = 1.0
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-RMSNorm Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
