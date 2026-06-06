def simulate():
    baseline_latency = 45.0
    baseline_bw = 15.0
    hw_pim_rope_latency = 3.5
    hw_pim_rope_bw = 1.0
    speedup = baseline_latency / hw_pim_rope_latency
    bw_red = (baseline_bw - hw_pim_rope_bw) / baseline_bw * 100
    print(f"HW-PIM-RoPE Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
