import numpy as np

def simulate_qkn_fuser(seq_len=65536, d_model=4096):
    # Baseline: Query/Key Normalization (RMSNorm) done in software
    # Requires an extra SRAM read/write pass for variance computation and normalization
    baseline_sram_reads_mb = (seq_len * d_model * 2 * 2) / (1024 * 1024) # Read Q/K, Read again to norm
    baseline_latency_ms = (baseline_sram_reads_mb / 64.0) * 1000 + 4.5 # Kernel overhead
    
    # HW-QKNF: Hardware QK-Norm Fuser
    # Computes RMSNorm directly at the register level as Q/K exit the projection MACs
    proposed_sram_reads_mb = (seq_len * d_model * 2) / (1024 * 1024) # Only write normalized Q/K once
    proposed_latency_ms = (proposed_sram_reads_mb / 64.0) * 1000 + 0.5 # HW overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline QK-Norm Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-QKNF Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SRAM Bandwidth Reduction: {(1 - proposed_sram_reads_mb/baseline_sram_reads_mb)*100:.2f}%")

simulate_qkn_fuser()
