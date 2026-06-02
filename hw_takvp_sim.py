import math

def simulate_hw_takvp(seq_len, attention_heads, kv_dim, cxl_bandwidth_gbps):
    print(f"Simulating Hardware Token-Adaptive KV Pruner (HW-TAKVP)")
    print(f"Seq Len: {seq_len}, Heads: {attention_heads}")
    
    # Baseline: Software based dynamic pruning logic
    baseline_latency_ms = (seq_len * attention_heads * kv_dim * 2 / (cxl_bandwidth_gbps * 1024**3)) * 1000 + 2.0 # 2ms software overhead
    
    # HW-TAKVP: Hardware inline pruning
    pruning_ratio = 0.85 # Prune 85% of tokens
    takvp_latency_ms = (seq_len * attention_heads * kv_dim * 2 * (1 - pruning_ratio) / (cxl_bandwidth_gbps * 1024**3)) * 1000 + 0.1 # 0.1ms hardware latency
    
    speedup = baseline_latency_ms / takvp_latency_ms if takvp_latency_ms > 0 else float('inf')
    
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-TAKVP Latency: {takvp_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Pruning Ratio: {pruning_ratio*100:.1f}%")

if __name__ == "__main__":
    simulate_hw_takvp(262144, 32, 128, 64)
