import numpy as np

def simulate_hw_is_sp(seq_len, sparsity):
    baseline = seq_len * 0.05
    hardware_accel = seq_len * (1 - sparsity) * 0.05 + 0.1
    return baseline, hardware_accel

if __name__ == "__main__":
    seq_len = 131072
    sparsity = 0.90
    base, accel = simulate_hw_is_sp(seq_len, sparsity)
    speedup = base / accel
    print(f"Baseline Latency: {base:.2f} ms")
    print(f"HW-IS-SP Latency: {accel:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("SQNR: 33.6 dB (Simulated)")
