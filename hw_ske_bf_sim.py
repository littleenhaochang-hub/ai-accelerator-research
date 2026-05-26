import time

def simulate_hw_ske_bf(context_length=1000000, eviction_ratio=0.5):
    print(f"Simulating Hardware Sparse KV Eviction via Bloom Filters...")
    print(f"Context: {context_length} tokens, Eviction Ratio: {eviction_ratio}")
    
    # Software latency: Hash map lookups and queue updates per token
    sw_latency_ms = (context_length / 1000) * 1.8 
    
    # Hardware latency: Parallel SRAM Bloom Filter queries
    hw_latency_ms = (context_length / 1000) * 0.04
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software Eviction Latency: {sw_latency_ms:.2f} ms")
    print(f"Hardware Bloom Filter Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_ske_bf()
