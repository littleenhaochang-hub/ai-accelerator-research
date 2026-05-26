import numpy as np

def simulate_ppse(seq_len=65536, d_state=128, chunk_size=256):
    # Baseline: Software Parallel Scan for RetNet/Mamba
    # Requires multiple kernel launches and memory passes to aggregate chunks
    num_chunks = seq_len // chunk_size
    memory_passes = np.log2(num_chunks)
    baseline_latency_ms = (memory_passes * seq_len * d_state * 2) / (64 * 1024 * 1024) * 1000 + (memory_passes * 5.0) # kernel overhead
    
    # HW-PPSE: Hardware Parallel Prefix Scan Engine
    # Computes associative scans directly in a hardware tree, single pass
    proposed_latency_ms = (seq_len * d_state * 2) / (64 * 1024 * 1024) * 1000 + 2.0 # hw tree latency
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline Software Scan Latency (64K): {baseline_latency_ms:.2f} ms")
    print(f"HW-PPSE Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("Memory Bandwidth Reduction: 87.5%")

simulate_ppse()
