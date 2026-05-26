import time

def simulate_hw_chunked_rope(context_length=128000, chunk_size=4096):
    print(f"Simulating Hardware Chunked RoPE Engine...")
    print(f"Context: {context_length} tokens, Chunk Size: {chunk_size}")
    
    # Software overhead: computing RoPE across full sequence dynamically
    sw_latency_ms = (context_length / 1000) * 1.25 
    
    # Hardware latency: computing RoPE per chunk and caching sine/cosine in SRAM
    num_chunks = context_length / chunk_size
    hw_latency_ms = num_chunks * 0.15
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software RoPE Latency: {sw_latency_ms:.2f} ms")
    print(f"HW Chunked RoPE Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_chunked_rope()
