import time
import math

def simulate_moe_decode(tokens=128, experts=8, expert_size_mb=500, pcie_bw_gbps=32):
    # Baseline: demand fetching
    fetch_time_ms = (expert_size_mb / 1024) / pcie_bw_gbps * 1000
    baseline_latency = tokens * fetch_time_ms
    
    # Proposed: Asynchronous DMA with Lookahead Predictor (simulated)
    # Assume 90% overlap
    proposed_latency = tokens * (fetch_time_ms * 0.1)
    
    speedup = baseline_latency / proposed_latency
    print(f"Tokens: {tokens}, Experts: {experts}")
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency (Async Lookahead): {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_moe_decode()
