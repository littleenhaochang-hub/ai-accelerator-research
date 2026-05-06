import time
import math

def simulate_hw_tome_kv():
    context_length = 32768
    hidden_size = 4096
    
    # Baseline: Writing all tokens to SRAM KV Cache
    baseline_kv_size_mb = (context_length * hidden_size * 2 * 2) / (1024 * 1024) # 2 bytes per param (FP16), K and V
    baseline_sram_write_latency_ms = baseline_kv_size_mb / 2.0 # Assume 2GB/s SRAM write bandwidth for simplicity
    
    # HW-ToMe-KV: Hardware Token Merging (merging 50% of tokens dynamically)
    merge_ratio = 0.5
    tome_kv_size_mb = baseline_kv_size_mb * (1 - merge_ratio)
    
    # Compute overhead of inline similarity check (hardware cosine sim)
    hw_sim_overhead_ms = 1.5 
    
    tome_sram_write_latency_ms = (tome_kv_size_mb / 2.0) + hw_sim_overhead_ms
    
    print("=== HW-ToMe-KV Simulation ===")
    print(f"Baseline KV Cache Size: {baseline_kv_size_mb:.2f} MB")
    print(f"HW-ToMe KV Cache Size: {tome_kv_size_mb:.2f} MB")
    print(f"Baseline Write Latency: {baseline_sram_write_latency_ms:.2f} ms")
    print(f"HW-ToMe Write Latency: {tome_sram_write_latency_ms:.2f} ms")
    
    speedup = baseline_sram_write_latency_ms / tome_sram_write_latency_ms
    print(f"Speedup: {speedup:.2f}x")
    print(f"Memory Reduction: {baseline_kv_size_mb / tome_kv_size_mb:.2f}x")

if __name__ == '__main__':
    simulate_hw_tome_kv()
