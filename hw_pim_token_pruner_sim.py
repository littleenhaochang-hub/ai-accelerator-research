def simulate():
    baseline_latency = 80.0
    baseline_bw = 24.0
    hw_pim_latency = 11.0
    hw_pim_bw = 4.8
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-TP Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
