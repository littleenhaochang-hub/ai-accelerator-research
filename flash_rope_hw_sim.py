import time

def standard_rope_compute(seq_len, d_head):
    # Simulated latency for standard Rotary Position Embedding
    # Requires complex sine/cosine multiplications in software/ALU
    flops = seq_len * d_head * 4
    latency = flops * 0.0005 # ms
    return latency

def flash_rope_hw_compute(seq_len, d_head):
    # Simulated latency for a dedicated Flash-RoPE CORDIC-based engine
    # Performed on the fly during the SRAM fetch
    latency = seq_len * d_head * 0.00005 # ms
    return latency

def main():
    seq_len = 16384
    d_head = 128
    
    print("Running Hardware Flash-RoPE Engine Simulation...")
    std_lat = standard_rope_compute(seq_len, d_head)
    print(f"Standard RoPE Latency: {std_lat:.2f} ms")
    
    hw_lat = flash_rope_hw_compute(seq_len, d_head)
    print(f"Hardware Flash-RoPE Latency: {hw_lat:.2f} ms")
    
    speedup = std_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
