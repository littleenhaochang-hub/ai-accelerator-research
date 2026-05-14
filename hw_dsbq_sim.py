import time

def simulate_standard_int4_fetch(params_billions):
    # Fetching INT4 (4 bits per param)
    bytes_to_fetch = (params_billions * 1e9 * 0.5) 
    bandwidth = 100e9 # 100 GB/s Edge memory bandwidth
    return bytes_to_fetch / bandwidth

def simulate_dsbq_158bit_fetch(params_billions):
    # Fetching 1.58-bit ternary weights packed into sub-bytes
    bytes_to_fetch = (params_billions * 1e9 * (1.58 / 8.0))
    bandwidth = 100e9
    hardware_decompress_overhead = 0.0015 # 1.5ms overhead for inline decompression
    return (bytes_to_fetch / bandwidth) + hardware_decompress_overhead

if __name__ == "__main__":
    params = 7 # 7B model
    
    t_int4 = simulate_standard_int4_fetch(params)
    t_dsbq = simulate_dsbq_158bit_fetch(params)
    
    print(f"Standard INT4 Fetch Latency: {t_int4:.4f} s")
    print(f"HW-DSBQ 1.58-bit Latency: {t_dsbq:.4f} s")
    print(f"Speedup: {t_int4 / t_dsbq:.2f}x")
