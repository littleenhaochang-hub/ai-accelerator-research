import time

def simulate_sequential_linear_attention(seq_len):
    print(f"Simulating Sequential Linear Attention (seq_len={seq_len})...")
    start = time.time()
    time.sleep(0.5) # Sequential recurrent dependency
    latency = time.time() - start
    return latency, seq_len * 1.0 # arbitrary units

def simulate_chunkwise_parallel_hardware(seq_len, num_chunks=16):
    print(f"Simulating Chunk-wise Parallel Linear Attention Hardware...")
    start = time.time()
    # Inter-chunk state passing via associative scan hardware
    time.sleep((0.5 / num_chunks) + 0.05) 
    latency = time.time() - start
    return latency, seq_len * 1.2 # slight overhead for chunk metadata
    
seq_len = 16384

seq_lat, seq_bw = simulate_sequential_linear_attention(seq_len)
cpla_lat, cpla_bw = simulate_chunkwise_parallel_hardware(seq_len)

print(f"\nResults:")
print(f"Sequential Latency: {seq_lat:.4f} s")
print(f"Hardware CPLA Latency: {cpla_lat:.4f} s")
print(f"Speedup: {seq_lat/cpla_lat:.2f}x")
