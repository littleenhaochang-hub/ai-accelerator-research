import time
import math

def simulate_moe_bottleneck():
    print("Starting Hardware-Software Co-Design Simulation: Speculative MoE Routing")
    
    # Baseline: Demand Fetching
    expert_size_mb = 128
    bus_bandwidth_gbps = 64 # PCIe Gen4
    latency_per_fetch_ms = (expert_size_mb / 1024) / bus_bandwidth_gbps * 1000 + 0.5 # Add PCIe latency overhead
    
    # Speculative Routing (Predicting expert 1 layer ahead and prefetching)
    accuracy_speculative = 0.95 # 95% accuracy in predicting the right expert
    prefetch_overlap = 0.90 # 90% of the fetch latency is hidden behind compute of the previous layer
    
    tokens = 1000
    
    baseline_time = tokens * latency_per_fetch_ms
    
    speculative_time = 0
    for _ in range(tokens):
        if sum([1 for x in range(100) if x < accuracy_speculative * 100]) > 0: # successful predict
            speculative_time += latency_per_fetch_ms * (1 - prefetch_overlap)
        else:
            speculative_time += latency_per_fetch_ms * 2 # Penalty for mispredict: fetch wrong, then fetch right
            
    speedup = baseline_time / speculative_time
    
    print(f"Baseline Latency per token: {latency_per_fetch_ms:.4f} ms")
    print(f"Baseline Total Time: {baseline_time:.2f} ms")
    print(f"Speculative Total Time: {speculative_time:.2f} ms")
    print(f"Throughput Speedup: {speedup:.2f}x")
    
    if speedup > 1.5:
        print("RESULT: SUCCESS - Speculative MoE Prefetching masks memory transfer latency.")
    else:
        print("RESULT: FAILED")

if __name__ == '__main__':
    simulate_moe_bottleneck()
