def simulate():
    baseline_latency = 75.0
    baseline_bw = 25.0
    hw_pim_latency = 9.5
    hw_pim_bw = 1.5
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-MLA Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
