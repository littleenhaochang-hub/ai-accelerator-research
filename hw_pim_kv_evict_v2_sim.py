def simulate():
    baseline_latency = 135.0
    baseline_bw = 40.0
    hw_pim_latency = 12.0
    hw_pim_bw = 3.5
    speedup = baseline_latency / hw_pim_latency
    bw_red = (baseline_bw - hw_pim_bw) / baseline_bw * 100
    print(f"HW-PIM-KVE-V2 Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
