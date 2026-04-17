import numpy as np

def simulate_kivi_hardware():
    print("Starting KIVI 2-bit KV Cache Hardware Simulation...")
    
    seq_len = 32768
    dim = 4096
    
    # Baseline: FP16 KV Cache
    baseline_kv_bytes = seq_len * dim * 2 * 2
    
    # KIVI: 2-bit KV Cache
    # Assumes asymmetric quantization per channel/token
    # 2 bits = 0.25 bytes
    # Plus scale and zero point (e.g., FP16 per group of 32)
    group_size = 32
    num_groups = dim // group_size
    
    kivi_data_bytes = seq_len * dim * 2 * 0.25
    kivi_meta_bytes = seq_len * num_groups * 2 * 2 * 2 # scales and zeros
    
    total_kivi_bytes = kivi_data_bytes + kivi_meta_bytes
    
    memory_reduction = (1 - total_kivi_bytes / baseline_kv_bytes) * 100
    
    # Simulation of bandwidth
    bandwidth_GBps = 150
    baseline_latency_ms = (baseline_kv_bytes / 1e9) / bandwidth_GBps * 1000
    kivi_latency_ms = (total_kivi_bytes / 1e9) / bandwidth_GBps * 1000
    
    print(f"Context Length: {seq_len}")
    print(f"Baseline FP16 KV Cache: {baseline_kv_bytes / 1e6:.2f} MB")
    print(f"KIVI 2-bit KV Cache (data + meta): {total_kivi_bytes / 1e6:.2f} MB")
    print(f"Memory Reduction: {memory_reduction:.2f}%")
    print(f"Effective Bandwidth Speedup: {baseline_latency_ms / kivi_latency_ms:.2f}x")
    print("Conclusion: 2-bit KV cache quantization offers an ~80% memory footprint reduction. Hardware requires a dedicated '2-bit KV Decompressor' inside the Attention block to prevent stalling.")

if __name__ == "__main__":
    simulate_kivi_hardware()