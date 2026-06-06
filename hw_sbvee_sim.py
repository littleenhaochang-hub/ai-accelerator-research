import math

def simulate_hw_sbvee(matrix_size_mb, sram_bandwidth_gbps):
    print(f"Simulating Hardware Sub-Byte Vector Expansion Engine (HW-SBVEE)")
    print(f"Base Matrix Size: {matrix_size_mb} MB (INT8 equivalent)")
    
    # Baseline INT4 fetch
    int4_transfer_mb = matrix_size_mb * 0.5
    baseline_latency_ms = (int4_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.5
    
    # HW-SBVEE: 1.58-bit ternary packed fetch + zero-cycle inline expansion
    ternary_transfer_mb = matrix_size_mb * (1.58 / 8.0)
    sbvee_latency_ms = (ternary_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.05
    
    speedup = baseline_latency_ms / sbvee_latency_ms if sbvee_latency_ms > 0 else float('inf')
    
    print(f"Baseline INT4 Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-SBVEE Latency: {sbvee_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SRAM Bandwidth Reduction: {(1 - ternary_transfer_mb/int4_transfer_mb)*100:.2f}%")

if __name__ == "__main__":
    simulate_hw_sbvee(1024, 2048)
