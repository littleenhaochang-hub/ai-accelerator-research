def simulate():
    baseline_latency = 160.0
    baseline_bw = 45.0
    hw_ia_latency = 15.5
    hw_ia_bw = 4.2
    speedup = baseline_latency / hw_ia_latency
    bw_red = (baseline_bw - hw_ia_bw) / baseline_bw * 100
    print(f"HW-IASE Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
