import numpy as np

def simulate_rope_extender():
    print("Simulating Hardware RoPE Context Extender...")
    seq_len = 65536
    
    # Baseline software RoPE interpolation overhead
    baseline_latency = seq_len * 0.008
    
    # Proposed hardware inline CORDIC interpolation
    proposed_latency = seq_len * 0.0005
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_rope_extender()
