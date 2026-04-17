import numpy as np
import math

def simulate_mamba_parallel_scan(seq_len=8192, state_dim=128, alu_latency_ns=1.0):
    print("=== Mamba/SSM Hardware Parallel Scan Simulation ===")
    print(f"Sequence Length: {seq_len}, State Dim: {state_dim}")
    
    # Baseline: Sequential Scan (RNN-like)
    # Latency scales linearly with sequence length (O(N) sequential steps)
    sequential_steps = seq_len
    baseline_latency_ns = sequential_steps * alu_latency_ns
    
    # Proposed: Hardware Parallel Prefix Sum Tree (Associative Scan)
    # Latency scales logarithmically with sequence length (O(log N) tree depth)
    # Assumes enough ALUs (N/2) to compute levels in parallel
    tree_depth = math.ceil(math.log2(seq_len))
    proposed_latency_ns = tree_depth * alu_latency_ns * 2 # up-sweep and down-sweep
    
    speedup = baseline_latency_ns / proposed_latency_ns
    
    print(f"[Baseline] Sequential Scan Latency: {baseline_latency_ns:.2f} ns")
    print(f"[Proposed] Parallel Prefix Tree Latency: {proposed_latency_ns:.2f} ns")
    print(f"Hardware Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_mamba_parallel_scan()
