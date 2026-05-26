import math

def simulate_hpmbe():
    # Baseline: Sequential evaluation of Mamba blocks in software
    num_blocks = 32
    seq_len = 1024
    baseline_latency_ms = (num_blocks * seq_len * 0.05) # 50us per block per token

    # Proposed: HW-PMBE (Hardware Parallel Mamba Block Evaluator)
    # Evaluates independent chunked states in parallel across blocks
    parallel_factor = 4
    proposed_latency_ms = (num_blocks * seq_len * 0.05) / parallel_factor + 0.1 # overhead

    speedup = baseline_latency_ms / proposed_latency_ms

    print(f"Simulation Complete: HW-PMBE (Hardware Parallel Mamba Block Evaluator)")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hpmbe()