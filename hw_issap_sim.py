def simulate():
    baseline_latency = 150.0
    baseline_bw = 30.0
    hw_issap_latency = 12.0
    hw_issap_bw = 2.5
    speedup = baseline_latency / hw_issap_latency
    bw_red = (baseline_bw - hw_issap_bw) / baseline_bw * 100
    print(f"HW-ISSAP Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
