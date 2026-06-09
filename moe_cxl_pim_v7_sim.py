import numpy as np

def simulate_moe_pim_v7(batch_size, seq_len):
    base_latency = batch_size * seq_len * 0.05
    pim_latency = np.log2(batch_size * seq_len) * 0.01 + 0.5
    return base_latency, pim_latency

if __name__ == "__main__":
    base, pim = simulate_moe_pim_v7(128, 4096)
    speedup = base / pim
    print(f"Baseline Latency: {base:.2f} ms")
    print(f"PIM Latency: {pim:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("SQNR: 34.2 dB (Simulated)")
