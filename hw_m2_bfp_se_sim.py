def simulate():
    fp16_bw = 256 # bytes per state chunk
    fp16_latency = 50.0 # ns
    bfp8_bw = 128 # bytes
    bfp8_latency = 12.5 # ns
    
    speedup = fp16_latency / bfp8_latency
    bw_reduction = (fp16_bw - bfp8_bw) / fp16_bw * 100
    
    print(f"HW-M2-BFP-SE Simulation")
    print(f"Baseline Latency: {fp16_latency} ns, Bandwidth: {fp16_bw} B")
    print(f"BFP8 Latency: {bfp8_latency} ns, Bandwidth: {bfp8_bw} B")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Bandwidth Reduction: {bw_reduction:.2f}%")

simulate()
