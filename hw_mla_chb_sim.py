import numpy as np

def simulate_mla_chb(seq_len=65536, num_heads=128, head_dim=128):
    # Baseline: DeepSeek MLA in Software
    # Software fetches the latent vector for EACH head independently due to lack of multicast
    baseline_dram_reads_mb = (seq_len * num_heads * head_dim * 2) / (1024 * 1024)
    baseline_latency_ms = (baseline_dram_reads_mb / 64.0) * 1000 + 15.0 # Kernel overhead
    
    # HW-MLA-CHB: Hardware MLA Cross-Head Broadcasting Bus
    # SRAM fetches the latent vector ONCE and broadcasts it to all Head ALUs simultaneously
    proposed_dram_reads_mb = (seq_len * head_dim * 2) / (1024 * 1024)
    proposed_latency_ms = (proposed_dram_reads_mb / 64.0) * 1000 + 1.0 # Hardware broadcast overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline MLA Fetch Latency (64K): {baseline_latency_ms:.2f} ms")
    print(f"HW-MLA-CHB Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SRAM Read Bandwidth Reduction: {(1 - proposed_dram_reads_mb/baseline_dram_reads_mb)*100:.2f}%")

simulate_mla_chb()
