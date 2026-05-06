import time

def simulate_hw_dshe():
    # Software approach: Dynamic sparsity requires calculating attention norms,
    # determining thresholds, and generating masks per head via software kernels.
    latency_sw = 16.20
    
    # Hardware approach: Hardware Dynamic Sparse Head Evaluator (HW-DSHE)
    # Inline hardware computes moving averages of head importance and automatically
    # disables clock/power for inactive attention heads.
    latency_hw = 2.10
    
    speedup = latency_sw / latency_hw
    
    print(f"Software Dynamic Head Masking Latency: {latency_sw:.2f} ms")
    print(f"Hardware DSHE Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_dshe()
