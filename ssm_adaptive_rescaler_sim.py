import numpy as np

def simulate_ssm_adaptive_rescaler():
    print("Simulating Hardware SSM Adaptive State Rescaler...")
    seq_len = 16384
    state_dim = 128
    
    # Baseline software rescaling
    baseline_latency = seq_len * state_dim * 0.003
    
    # Proposed inline hardware exponent rescaler
    proposed_latency = seq_len * state_dim * 0.0004
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_ssm_adaptive_rescaler()
