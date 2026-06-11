import time
import random

def simulate_gpu_baseline_mamba(draft_len):
    # Standard Mamba autoregressive generation is memory bound
    start = time.time()
    for _ in range(draft_len):
        time.sleep(0.0001)  # High memory access overhead
    return time.time() - start

def simulate_specmamba_fpga(draft_len):
    # SpecMamba applies speculative decoding with FIFO-based tree verification 
    # Parallel linear layers and serial SSM layers
    start = time.time()
    # Draft generation
    time.sleep(0.00002 * draft_len)
    # Verification with tiling to minimize memory access
    time.sleep(0.00001) 
    return time.time() - start

if __name__ == "__main__":
    draft_length = 64
    gpu_time = simulate_gpu_baseline_mamba(draft_length)
    specmamba_time = simulate_specmamba_fpga(draft_length)
    
    speedup = gpu_time / specmamba_time if specmamba_time > 0 else float('inf')
    print(f"GPU Baseline Latency: {gpu_time*1000:.2f} ms")
    print(f"SpecMamba FPGA Latency: {specmamba_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
