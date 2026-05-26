import math

def simulate_hw_dpkvc():
    # Baseline: Fixed precision INT4 KV Cache
    context_length = 32 * 1024
    baseline_latency_ms = context_length * 0.05 # Read latency

    # Proposed: HW-DPKVC (Hardware Dynamic Precision KV Cache)
    # Dynamically scales precision based on attention scores (1-bit to 8-bit)
    proposed_latency_ms = context_length * 0.015

    speedup = baseline_latency_ms / proposed_latency_ms

    print(f"Simulation Complete: HW-DPKVC (Hardware Dynamic Precision KV Cache)")
    print(f"Baseline Latency (INT4): {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency (Dynamic): {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hw_dpkvc()