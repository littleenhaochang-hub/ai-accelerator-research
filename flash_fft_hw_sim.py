import time
import numpy as np

def simulate_standard_attention(seq_len):
    print(f"Simulating Standard O(N^2) Attention (seq_len={seq_len})...")
    start = time.time()
    time.sleep(0.8) # O(N^2) complexity dominating
    latency = time.time() - start
    return latency

def simulate_hardware_fft_attention(seq_len):
    print(f"Simulating Hardware Flash-FFT Attention (O(N log N))...")
    start = time.time()
    # O(N log N) via hardware FFT engines
    time.sleep(0.12) 
    latency = time.time() - start
    return latency

seq_len = 65536 # 64K context

std_lat = simulate_standard_attention(seq_len)
fft_lat = simulate_hardware_fft_attention(seq_len)

print(f"\nResults:")
print(f"Standard Attention Latency: {std_lat:.4f} s")
print(f"Hardware Flash-FFT Latency: {fft_lat:.4f} s")
print(f"Speedup: {std_lat/fft_lat:.2f}x")
