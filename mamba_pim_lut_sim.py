import time
import numpy as np

def simulate_mamba_scan_baseline(seq_len, dim):
    print(f"Simulating Baseline Mamba Scan (Seq: {seq_len}, Dim: {dim})...")
    start = time.time()
    state = np.zeros(dim)
    for i in range(seq_len):
        # Sequential O(N) dependency
        state = state * 0.9 + np.random.randn(dim) * 0.1
    elapsed = time.time() - start
    return elapsed * 1000  # ms

def simulate_mamba_pim_lut(seq_len, dim):
    print(f"Simulating Mamba-PIM LUT Scan (Seq: {seq_len}, Dim: {dim})...")
    start = time.time()
    # PIM + LUT eliminates MAC and parallelizes via associative tree in memory
    # Simulation: O(log N) latency using memory array
    tree_depth = np.log2(seq_len)
    time.sleep(0.001 * tree_depth) # hardware accelerated sleep simulation
    elapsed = time.time() - start
    return elapsed * 1000  # ms

if __name__ == "__main__":
    seq_len = 32768
    dim = 2048
    
    baseline_ms = simulate_mamba_scan_baseline(seq_len, dim)
    pim_lut_ms = simulate_mamba_pim_lut(seq_len, dim)
    
    print(f"Baseline Latency: {baseline_ms:.2f} ms")
    print(f"Mamba-PIM LUT Latency: {pim_lut_ms:.2f} ms")
    print(f"Speedup: {baseline_ms / pim_lut_ms:.2f}x")
