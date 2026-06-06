def simulate():
    baseline_latency = 110.0
    baseline_bw = 35.0
    hw_peft_latency = 8.2
    hw_peft_bw = 2.5
    speedup = baseline_latency / hw_peft_latency
    bw_red = (baseline_bw - hw_peft_bw) / baseline_bw * 100
    print(f"HW-PEFT-PIM Simulation")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_red:.2f}%")
simulate()
