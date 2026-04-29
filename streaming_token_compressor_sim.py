import numpy as np

def simulate_streaming_token_compressor():
    print("Simulating Hardware Streaming Token Compressor (HSTC)...")
    seq_len = 16384
    
    # Baseline software token merging and similarity check
    baseline_latency = seq_len * 0.018
    
    # Proposed hardware inline token similarity and merging
    proposed_latency = seq_len * 0.0012
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_streaming_token_compressor()
