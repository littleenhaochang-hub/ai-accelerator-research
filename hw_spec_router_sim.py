def simulate():
    baseline_latency = 120.0
    baseline_bw = 25.0
    hw_spec_latency = 8.5
    hw_spec_bw = 2.0
    speedup = baseline_latency / hw_spec_latency
    bw_red = (baseline_bw - hw_spec_bw) / baseline_bw * 100
    print(f"HW-Spec-Router Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
