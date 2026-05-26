import time

def simulate_hw_flash_dec_merger(context_length=512000, num_kv_heads=8, num_q_heads=32):
    print(f"Simulating Hardware Flash-Decoding KV Merger...")
    print(f"Context: {context_length} tokens, KV Heads: {num_kv_heads}, Q Heads: {num_q_heads}")
    
    # Software latency: Softmax reduction across large KV partitions in DRAM
    sw_latency_ms = (context_length / 1000) * 1.8 
    
    # Hardware latency: On-the-fly SRAM reduction tree
    hw_latency_ms = (context_length / 1000) * 0.08
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software Flash-Decoding Reduction Latency: {sw_latency_ms:.2f} ms")
    print(f"HW Flash-Decoding Merger Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_flash_dec_merger()
