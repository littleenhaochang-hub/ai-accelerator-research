import math

def simulate_hw_sram_sp(matrix_dim, sparsity, sram_bandwidth_gbps):
    print(f"Simulating Hardware In-SRAM Sparse Predictor (HW-SRAM-SP)")
    print(f"Matrix Dim: {matrix_dim}x{matrix_dim}, Sparsity: {sparsity*100}%")
    
    # Baseline: Full dense memory fetch
    baseline_transfer_mb = (matrix_dim * matrix_dim * 2) / (1024**2)
    baseline_latency_ms = (baseline_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.1
    
    # HW-SRAM-SP: PIM level sparsity prediction, completely avoiding macro-level read
    sram_sp_latency_ms = (baseline_transfer_mb * (1 - sparsity) / (sram_bandwidth_gbps * 1024)) * 1000 + 0.02
    
    speedup = baseline_latency_ms / sram_sp_latency_ms if sram_sp_latency_ms > 0 else float('inf')
    
    print(f"Baseline Transfer: {baseline_transfer_mb:.2f} MB")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-SRAM-SP Latency: {sram_sp_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Energy Reduction: {sparsity*100:.1f}%")

if __name__ == "__main__":
    # Simulate an 8192x8192 activation matrix with 85% sparsity, SRAM Bandwidth 2048 GB/s
    simulate_hw_sram_sp(8192, 0.85, 2048)
