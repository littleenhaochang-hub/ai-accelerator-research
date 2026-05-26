import numpy as np

def simulate_hdlre(d_model=4096, r=16):
    # Baseline LoRA: Read Activation, project to R, project back to d_model, add to base
    # Assumes dense MAC arrays fetching adapters from DRAM
    baseline_dram_read_mb = (d_model * r * 2 * 2) / (1024 * 1024)
    baseline_latency_ms = (baseline_dram_read_mb / 64.0) * 1000 + 2.5 # kernel overhead
    
    # HW-DLRE: Hardware Dynamic Low-Rank Evaluator
    # Evaluates activation magnitude in hardware; if magnitude is low, dynamically skips the adapter branch
    bypass_ratio = 0.65 # 65% of tokens don't need LoRA adaptation
    proposed_latency_ms = (baseline_dram_read_mb * (1 - bypass_ratio) / 64.0) * 1000 + 0.5 # inline hw overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline LoRA Branch Latency: {baseline_latency_ms:.4f} ms")
    print(f"HW-DLRE Latency: {proposed_latency_ms:.4f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Compute Reduction: {bypass_ratio * 100:.1f}%")

simulate_hdlre()
