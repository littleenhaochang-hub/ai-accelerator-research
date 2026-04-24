import time

def standard_gemm_activation(batch_size, hidden_size):
    # Simulated latency for separate GEMM and activation passes
    # 1. Read input, compute GEMM, write to SRAM
    # 2. Read from SRAM, compute Activation (e.g., SwiGLU), write to SRAM
    gemm_lat = batch_size * hidden_size * 0.005 # ms
    act_lat = batch_size * hidden_size * 0.002 # ms
    return gemm_lat + act_lat

def fused_gemm_activation(batch_size, hidden_size):
    # Simulated latency for Fused GEMM + Activation
    # Computed on the fly as the MAC results leave the accumulator
    fused_lat = batch_size * hidden_size * 0.0051 # ms (slight overhead for inline compute)
    return fused_lat

def main():
    batch_size = 4096
    hidden_size = 4096
    
    print("Running Hardware Fused GEMM+Activation Simulation...")
    std_lat = standard_gemm_activation(batch_size, hidden_size)
    print(f"Standard Separate Pass Latency: {std_lat:.2f} ms")
    
    hw_lat = fused_gemm_activation(batch_size, hidden_size)
    print(f"Fused Hardware Latency: {hw_lat:.2f} ms")
    
    speedup = std_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
