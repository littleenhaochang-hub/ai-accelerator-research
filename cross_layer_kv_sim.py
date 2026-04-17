import numpy as np

def simulate_cross_layer_kv():
    print("Starting Cross-Layer KV Cache (CLA) Hardware Simulation...")
    
    num_layers = 32
    seq_len = 8192
    dim = 4096
    
    # Baseline: KV cache for every layer
    baseline_kv_bytes = num_layers * seq_len * dim * 2 * 2 # 2 for K,V and 2 for 16-bit
    
    # CLA: Share KV cache across group of layers (e.g. group size = 4)
    group_size = 4
    num_groups = num_layers // group_size
    cla_kv_bytes = num_groups * seq_len * dim * 2 * 2
    
    memory_reduction = (1 - cla_kv_bytes / baseline_kv_bytes) * 100
    
    # Simulate routing logic latency overhead in hardware
    routing_latency_ns = 5 # 5ns per route
    total_routing_overhead_ns = seq_len * num_layers * routing_latency_ns
    
    # Bandwidth simulation
    bandwidth_GBps = 150
    baseline_latency_ms = (baseline_kv_bytes / 1e9) / bandwidth_GBps * 1000
    cla_latency_ms = (cla_kv_bytes / 1e9) / bandwidth_GBps * 1000 + (total_routing_overhead_ns / 1e6)
    
    print(f"Baseline KV Cache Memory: {baseline_kv_bytes / 1e6:.2f} MB")
    print(f"CLA KV Cache Memory: {cla_kv_bytes / 1e6:.2f} MB")
    print(f"Memory Reduction: {memory_reduction:.2f}%")
    print(f"Effective Speedup: {baseline_latency_ms / cla_latency_ms:.2f}x")
    print("Conclusion: Cross-Layer Attention reduces KV cache proportionally to group size. Hardware requires a 'KV Route Multiplexer' to broadcast the grouped KV caches to multiple attention layers concurrently.")

if __name__ == "__main__":
    simulate_cross_layer_kv()
