import time

def software_kv_compression(tokens, d_model):
    # Simulated latency for software-based Outlier-aware KV Cache compression (e.g. 8-bit or 4-bit)
    # Requires analyzing blocks, separating outliers, packing bits
    latency = tokens * d_model * 0.002 # ms
    return latency

def hardware_kv_compressor(tokens, d_model):
    # Simulated latency for an inline Hardware KV Cache Compressor
    # Compresses data on-the-fly via hardware bit-packing and outlier bypass
    latency = tokens * d_model * 0.0001 # ms
    return latency

def main():
    tokens = 16384
    d_model = 128
    
    print("Running Hardware KV Cache Compressor Simulation...")
    sw_lat = software_kv_compression(tokens, d_model)
    print(f"Software KV Compression Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_kv_compressor(tokens, d_model)
    print(f"Hardware KV Compression Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
