import time
import numpy as np

def simulate_adaptive_kv_sparsity(context_length, sparsity_ratio):
    print(f"Simulating Token-Adaptive KV Cache Sparsity for context length {context_length}...")
    baseline_macs = context_length ** 2
    baseline_latency = baseline_macs / 1e9  # arbitrary unit
    
    sparse_macs = baseline_macs * (1 - sparsity_ratio)
    sparse_latency = sparse_macs / 1e9
    
    # Simulate hardware routing overhead
    hw_overhead = 0.05 * baseline_latency 
    total_sparse_latency = sparse_latency + hw_overhead
    
    speedup = baseline_latency / total_sparse_latency
    sqnr = 35.0 - (sparsity_ratio * 5) # slight degradation
    
    print(f"Baseline Latency: {baseline_latency:.4f} s")
    print(f"Sparse Latency (inc. HW overhead): {total_sparse_latency:.4f} s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SQNR: {sqnr:.2f} dB")
    
    return speedup, sqnr

simulate_adaptive_kv_sparsity(128000, 0.75)
