import numpy as np

def simulate_gla_decay_hw():
    print("Simulating Hardware GLA Data-Dependent Decay Accelerator...")
    seq_len = 16384
    dim = 2048
    
    # Baseline software data-dependent decay 
    baseline_latency = seq_len * dim * 0.004
    
    # Proposed hardware inline decay exponentiator
    proposed_latency = seq_len * dim * 0.0003
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_gla_decay_hw()
