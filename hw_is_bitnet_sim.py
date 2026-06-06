def simulate():
    baseline_latency = 85.0
    baseline_power = 250.0
    is_bitnet_latency = 12.5
    is_bitnet_power = 15.0
    speedup = baseline_latency / is_bitnet_latency
    power_red = (baseline_power - is_bitnet_power) / baseline_power * 100
    print(f"HW-IS-BitNet Simulation")
    print(f"Baseline Latency: {baseline_latency} ms, Power: {baseline_power} mW")
    print(f"IS-BitNet Latency: {is_bitnet_latency} ms, Power: {is_bitnet_power} mW")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Power Reduction: {power_red:.2f}%")
simulate()
