import time

def standard_kv_cache(tokens, d_model):
    # Simulated SRAM memory footprint for full KV cache
    # 2 bytes per element (FP16)
    memory_kb = (tokens * d_model * 2 * 2) / 1024
    latency = tokens * 0.05
    return memory_kb, latency

def heavy_hitter_oracle_cache(tokens, d_model, retain_ratio=0.2):
    # Simulated SRAM footprint keeping only the top 20% heavy-hitters plus recent tokens
    memory_kb = (tokens * retain_ratio * d_model * 2 * 2) / 1024
    # Slight hardware sorting/tracking overhead
    latency = tokens * 0.012
    return memory_kb, latency

def main():
    tokens = 32768
    d_model = 128
    
    print("Running Hardware Heavy-Hitter Oracle Simulation...")
    std_mem, std_lat = standard_kv_cache(tokens, d_model)
    print(f"Standard KV Cache: {std_mem:.2f} KB, Latency: {std_lat:.2f} ms")
    
    hw_mem, hw_lat = heavy_hitter_oracle_cache(tokens, d_model)
    print(f"Heavy-Hitter Oracle Cache: {hw_mem:.2f} KB, Latency: {hw_lat:.2f} ms")
    
    compression = std_mem / hw_mem
    speedup = std_lat / hw_lat
    print(f"\nMemory Compression: {compression:.2f}x")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
