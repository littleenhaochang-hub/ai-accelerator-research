import time

def simulate_standard_mac_attention(seq_len, dim):
    # Standard MAC operations for attention
    return (seq_len * seq_len * dim) / 1e11

def simulate_matmul_free_attention(seq_len, dim):
    # Ternary accumulations + Hadamard transform
    # Replaces multipliers with hardware sign flips and additions (approx 8.5x efficiency gain)
    adder_delay = (seq_len * seq_len * dim) / (1e11 * 8.5)
    hadamard_overhead = (seq_len * dim) / 1e10
    return adder_delay + hadamard_overhead

if __name__ == "__main__":
    seq_len = 8192
    dim = 2048
    soft = simulate_standard_mac_attention(seq_len, dim)
    hw = simulate_matmul_free_attention(seq_len, dim)
    print(f"Standard MAC Latency: {soft:.4f} s")
    print(f"HW-MFLM Latency: {hw:.4f} s")
    print(f"Speedup: {soft/hw:.2f}x")
