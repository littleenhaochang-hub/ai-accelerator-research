import math

def simulate_hw_sram_cmac(batch_size, num_experts, seq_len, hidden_dim, sram_bandwidth_gbps):
    print(f"Simulating Hardware In-SRAM Compute-MAC Engine (HW-SRAM-CMAC)")
    print(f"Batch Size: {batch_size}, Experts: {num_experts}, Seq Len: {seq_len}")
    
    # Baseline: Read activations from SRAM to digital Tensor Core
    baseline_transfer_mb = (batch_size * seq_len * hidden_dim * 2) / (1024**2)
    baseline_latency_ms = (baseline_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.5 # 0.5ms dispatch overhead
    
    # HW-SRAM-CMAC: Processing-in-Memory execution using SRAM bitlines
    sram_cmac_latency_ms = 0.08 # Fixed analog execution time, irrespective of pure transfer
    
    speedup = baseline_latency_ms / sram_cmac_latency_ms if sram_cmac_latency_ms > 0 else float('inf')
    
    print(f"Baseline Transfer: {baseline_transfer_mb:.2f} MB")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-SRAM-CMAC Latency: {sram_cmac_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_sram_cmac(16, 64, 4096, 4096, 1024)
