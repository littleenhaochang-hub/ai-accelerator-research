import random

def simulate_software_hash_routing(num_tokens, num_experts):
    # Software routing involves matrix mult for logits then Top-K sorting
    # Simulated latency for pure software
    routing_latency_ms = num_tokens * num_experts * 0.000005 
    return routing_latency_ms

def simulate_hw_chr(num_tokens, num_experts):
    # Hardware Cuckoo Hash Router (HW-CHR)
    # Replaces sorting and inner products with an O(1) hardware hash lookup
    # Requires an offline-trained cluster embedding mapped to the hash table
    # Latency is strictly O(1) per token
    lookup_latency_ms = num_tokens * 0.0000001
    return lookup_latency_ms

if __name__ == "__main__":
    tokens = 8192
    experts = 1024 # Massive scale MoE
    
    sw_lat = simulate_software_hash_routing(tokens, experts)
    hw_lat = simulate_hw_chr(tokens, experts)
    
    speedup = sw_lat / hw_lat
    
    print(f"Software Routing Latency: {sw_lat:.2f} ms")
    print(f"HW-CHR Routing Latency: {hw_lat:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
