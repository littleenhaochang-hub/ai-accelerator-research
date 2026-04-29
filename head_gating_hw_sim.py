import time
import numpy as np

def simulate_dense_attention(seq_len, num_heads):
    print(f"Simulating baseline dense attention ({num_heads} heads, seq_len={seq_len})...")
    start = time.time()
    # Simulating memory-bound KV fetch
    time.sleep(0.5) 
    latency = time.time() - start
    return latency, num_heads * seq_len * 128 * 2

def simulate_gated_attention(seq_len, num_heads, active_ratio=0.25):
    print(f"Simulating hardware-gated attention (active ratio: {active_ratio})...")
    start = time.time()
    # Simulating fetching only active heads + minor hardware gating overhead
    time.sleep(0.5 * active_ratio + 0.05)
    latency = time.time() - start
    return latency, int(num_heads * active_ratio) * seq_len * 128 * 2

seq_len = 8192
num_heads = 32

dense_lat, dense_bw = simulate_dense_attention(seq_len, num_heads)
gated_lat, gated_bw = simulate_gated_attention(seq_len, num_heads)

print(f"\nResults:")
print(f"Dense Attention Latency: {dense_lat:.4f} s | Bandwidth: {dense_bw/1e6:.2f} MB")
print(f"Gated Attention Latency: {gated_lat:.4f} s | Bandwidth: {gated_bw/1e6:.2f} MB")
print(f"Speedup: {dense_lat/gated_lat:.2f}x")
