import time

def simulate_traditional_kv_dequant(seq_len):
    # Standard 4-bit KV Dequantization: Unaligned memory accesses and scalar dequantization
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000003) # Memory fetch + ALU dequantization penalty
    return time.time() - start

def simulate_innerq_kv_dequant(seq_len):
    # InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache
    # Grouping along the inner dimension to align dequantization with vector-matrix multiplication
    # Per-channel normalization folded into weights (zero runtime overhead)
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000001) # Faster vector-aligned fetch + reduced ALU overhead
    return time.time() - start

if __name__ == "__main__":
    seq_length = 32768
    
    trad_time = simulate_traditional_kv_dequant(seq_length)
    innerq_time = simulate_innerq_kv_dequant(seq_length)
    
    speedup = trad_time / innerq_time if innerq_time > 0 else float('inf')
    
    print(f"Traditional KV Dequantization Latency: {trad_time*1000:.2f} ms")
    print(f"InnerQ KV Dequantization Latency: {innerq_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
