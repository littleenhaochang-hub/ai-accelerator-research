import time

def simulate_traditional_mac(seq_len, hidden_dim):
    # Traditional INT8 MAC simulation
    start = time.time()
    for _ in range(seq_len):
        for _ in range(hidden_dim):
            # Simulate INT8 MAC delay
            time.sleep(0.000002)
    end = time.time()
    return end - start

def simulate_bitnet_lut(seq_len, hidden_dim):
    # LUT-based 1.58-bit inference simulation
    # Replaces complex multipliers with fast SRAM LUT + conditional additions
    start = time.time()
    for _ in range(seq_len):
        for _ in range(hidden_dim):
            # Simulate LUT lookup / conditional addition
            time.sleep(0.0000005)
    end = time.time()
    return end - start

if __name__ == "__main__":
    seq = 512
    dim = 256
    trad_time = simulate_traditional_mac(seq, dim)
    lut_time = simulate_bitnet_lut(seq, dim)
    
    speedup = trad_time / lut_time if lut_time > 0 else float('inf')
    print(f"Traditional INT8 MAC Latency: {trad_time*1000:.2f} ms")
    print(f"LUT-based BitNet 1.58b Latency: {lut_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
