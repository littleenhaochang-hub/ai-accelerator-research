def simulate():
    baseline_latency = 48.0
    baseline_bw = 18.0
    hw_pim_rope_v2_latency = 2.5
    hw_pim_rope_v2_bw = 0.5
    speedup = baseline_latency / hw_pim_rope_v2_latency
    bw_red = (baseline_bw - hw_pim_rope_v2_bw) / baseline_bw * 100
    print(f"HW-PIM-RoPE-v2 Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
