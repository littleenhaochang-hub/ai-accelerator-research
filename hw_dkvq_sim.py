import time

def simulate_static_kv_fetch(seq_len, batch_size):
    # Static 4-bit KV Cache fetch
    total_bits = seq_len * batch_size * 4096 * 4
    latency = total_bits / 1e11 # Memory bandwidth bound (100GB/s)
    return latency

def simulate_hw_dkvq_fetch(seq_len, batch_size):
    # Hardware Dynamic KV Quantization (1-bit for background, 4-bit for heavy hitters)
    heavy_hitter_ratio = 0.2
    avg_bits = (4 * heavy_hitter_ratio) + (1 * (1 - heavy_hitter_ratio))
    total_bits = seq_len * batch_size * 4096 * avg_bits
    latency = total_bits / 1e11
    hardware_overhead = 0.0005 # 500us
    return latency + hardware_overhead

if __name__ == "__main__":
    seq_len = 131072 # 128K context
    batch_size = 16
    
    static_time = simulate_static_kv_fetch(seq_len, batch_size)
    hw_dkvq_time = simulate_hw_dkvq_fetch(seq_len, batch_size)
    
    print(f"Static 4-bit KV Latency: {static_time:.4f} s")
    print(f"HW-DKVQ Dynamic Latency: {hw_dkvq_time:.4f} s")
    print(f"Speedup: {static_time / hw_dkvq_time:.2f}x")
