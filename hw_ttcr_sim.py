import math

def simulate_ttcr():
    # Baseline: Software-managed Test-Time Compute routing (e.g., MCTS node expansion)
    num_tokens = 1024
    # Software overhead involves GPU-CPU sync to determine if a token needs more thinking
    software_sync_ms = 0.5 
    baseline_latency_ms = num_tokens * software_sync_ms

    # Proposed: HW-TTCR (Hardware Test-Time Compute Router)
    # Inline hardware evaluator that checks confidence scores and triggers 
    # recursive logic or output generation without waking up the CPU.
    hardware_eval_ms = 0.002
    proposed_latency_ms = num_tokens * hardware_eval_ms

    speedup = baseline_latency_ms / proposed_latency_ms

    print(f"Simulation Complete: HW-TTCR (Hardware Test-Time Compute Router)")
    print(f"Baseline Latency (Software MCTS Routing): {baseline_latency_ms:.2f} ms")
    print(f"Proposed Latency (Hardware TTCR): {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_ttcr()