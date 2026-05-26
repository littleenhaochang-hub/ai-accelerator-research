import time

def simulate_hw_token_trimmer(context_length=128000, keep_ratio=0.2):
    print(f"Simulating Hardware Token Trimmer for {context_length} context...")
    
    # Software overhead
    sw_latency_ms = (context_length / 1000) * 0.5 
    
    # Hardware overhead (inline)
    hw_latency_ms = (context_length / 1000) * 0.01
    
    speedup = sw_latency_ms / hw_latency_ms
    memory_reduction = 1.0 / keep_ratio
    
    print(f"Software Trimming Latency: {sw_latency_ms:.2f} ms")
    print(f"Hardware Inline Trimming Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Memory Capacity Reduction: {memory_reduction:.2f}x")

if __name__ == "__main__":
    simulate_hw_token_trimmer()
