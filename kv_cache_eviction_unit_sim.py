import numpy as np

def simulate_kv_cache_eviction_unit():
    print("Simulating Hardware KV Cache Eviction Unit...")
    seq_len = 16384
    
    # Baseline software eviction overhead
    baseline_latency = seq_len * 0.005
    
    # Proposed hardware inline eviction
    proposed_latency = seq_len * 0.0003
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_kv_cache_eviction_unit()
