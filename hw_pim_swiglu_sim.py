def simulate():
    baseline_latency = 55.0
    baseline_bw = 20.0
    hw_pim_latency = 8.0
    hw_pim_bw = 2.0
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-SwiGLU Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
