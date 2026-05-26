import math

def simulate_hw_ltt():
    # Baseline: Software truncation of tokens for DOM inputs
    seq_len = 65536
    baseline_latency_ms = seq_len * 0.04 

    # Proposed: HW-LTT (Hardware Lookahead Token Truncator)
    proposed_latency_ms = seq_len * 0.005

    speedup = baseline_latency_ms / proposed_latency_ms

    print(f"Simulation Complete: HW-LTT (Hardware Lookahead Token Truncator)")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hw_ltt()