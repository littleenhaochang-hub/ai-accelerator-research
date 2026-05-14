import time
import random

def simulate_moe_decoding(tokens, prefetch_enabled):
    print(f"Simulating MoE decoding for {tokens} tokens. Prefetch enabled: {prefetch_enabled}")
    start_time = time.time()
    
    # Baseline PCIe latency per expert fetch: ~2.5ms
    # CXL NEP hardware prefetch latency exposed: ~0.1ms
    
    latency_per_token = 0.0
    for _ in range(tokens):
        if prefetch_enabled:
            # Most fetches are hidden, but occasionally we mispredict
            miss = random.random() < 0.05
            latency_per_token += 0.1 if not miss else 2.5
        else:
            latency_per_token += 2.5
            
    total_time = latency_per_token / 1000.0 # to seconds
    # Compute MAC time (negligible compared to memory)
    compute_time = tokens * 0.0005
    
    actual_time = total_time + compute_time
    
    print(f"Total time: {actual_time:.4f}s")
    return actual_time

baseline_time = simulate_moe_decoding(1000, False)
nep_time = simulate_moe_decoding(1000, True)

speedup = baseline_time / nep_time
print(f"Speedup: {speedup:.2f}x")
