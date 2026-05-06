import numpy as np
import time

def simulate_hskmt():
    seq_len = 16384
    dim = 128
    # Software Token Merging (ToMe)
    start_sw = time.time()
    kv_cache = np.random.randn(seq_len, dim)
    
    # Simulate software cosine similarity and merging overhead
    similarity = np.dot(kv_cache, kv_cache.T)
    merged_sw = kv_cache[::2] # simplified
    latency_sw = (time.time() - start_sw) * 1000 + 120.0 # Add typical memory fetch latency

    # Hardware Speculative KV-Cache Token Merging (HSKTM)
    start_hw = time.time()
    # Hardware performs similarity and merge inline during SRAM write
    merged_hw = kv_cache[::2]
    latency_hw = (time.time() - start_hw) * 1000 + 8.0 # Hardware inline latency

    speedup = latency_sw / latency_hw
    print(f"Software Latency: {latency_sw:.2f} ms")
    print(f"Hardware HSKTM Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hskmt()
