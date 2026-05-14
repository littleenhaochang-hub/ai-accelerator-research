import time

def simulate_software_mamba_ema(seq_len, state_dim):
    # Software Mamba state update: Read state, compute exponential decay via MACs, write state
    # O(N * D) memory bound
    dram_latency = (seq_len * state_dim * 2 * 2) / 1e10 # 100GB/s bandwidth assumption
    alu_latency = 0.015 # ALU transcendental overhead
    return dram_latency + alu_latency

def simulate_hw_mamba_ema(seq_len, state_dim):
    # Hardware In-SRAM Mamba EMA: Compute decay directly on SRAM bitlines (PIM)
    sram_latency = (seq_len * state_dim) / 1e12 # In-memory processing bandwidth
    return sram_latency

if __name__ == "__main__":
    seq_len = 32768
    state_dim = 4096 # Mamba hidden state size
    
    soft_time = simulate_software_mamba_ema(seq_len, state_dim)
    hw_time = simulate_hw_mamba_ema(seq_len, state_dim)
    
    print(f"Software Mamba EMA Latency: {soft_time:.4f} s")
    print(f"HW-Mamba-EMA Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
