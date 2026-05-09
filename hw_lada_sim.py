import time

def simulate_hw_lada():
    context_length = 32768
    hidden_dim = 2048
    state_dim = 2048
    
    # Baseline: Software execution of Gated Linear Attention (GLA) state update
    # Requires fetching State Matrix (2048x2048 FP16 = 8MB per layer), computing data-dependent
    # exponential decay (exp/sigmoid on ALU), and writing back.
    state_matrix_mb = (hidden_dim * state_dim * 2) / (1024 * 1024)
    sram_bw_gbps = 2000
    
    # 1. Read state, 2. FPU exp() compute, 3. Update, 4. Write state
    # Exponential compute is slow in standard MACs (often requires Taylor series or multiple cycles)
    fpu_exp_latency_ms = 0.005  # per token
    sram_rw_latency_ms = (state_matrix_mb * 2 / 1024) / sram_bw_gbps * 1000
    
    baseline_latency_ms = context_length * (sram_rw_latency_ms + fpu_exp_latency_ms)
    
    # HW-LADA: Hardware Linear Attention Decay Accelerator
    # Computes PWL (Piecewise Linear) approximation of exp() inline, and updates the state
    # matrix directly at the SRAM boundary (Near-Memory Processing). Zero MAC array intervention.
    pwl_latency_ms = 0.0005 # per token
    # SRAM RW is hidden behind the pipeline or severely reduced by inline processing
    hw_sram_rw_latency_ms = sram_rw_latency_ms * 0.1 
    
    hw_lada_latency_ms = context_length * (hw_sram_rw_latency_ms + pwl_latency_ms)
    
    print("=== HW-LADA Simulation ===")
    print(f"Context Length: {context_length}")
    print(f"Baseline Latency (Software GLA State Update): {baseline_latency_ms:.2f} ms")
    print(f"HW-LADA Latency (Inline PWL + NMP Update): {hw_lada_latency_ms:.2f} ms")
    print(f"Speedup: {baseline_latency_ms/hw_lada_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_lada()