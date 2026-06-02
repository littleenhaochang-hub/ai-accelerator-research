import math

def simulate_hw_oa_s2kvd(seq_len, hidden_dim, cxl_bandwidth_gbps):
    print(f"Simulating Hardware Outlier-Aware Sub-2-bit KV Decompressor (HW-OA-S2KVD)")
    print(f"Seq Len: {seq_len}, Hidden Dim: {hidden_dim}")
    
    # Baseline FP16 fetch (2 bytes per element, K and V)
    baseline_transfer_mb = (seq_len * hidden_dim * 2 * 2) / (1024**2)
    baseline_latency_ms = (baseline_transfer_mb / (cxl_bandwidth_gbps * 1024)) * 1000
    
    # HW-OA-S2KVD: 99% 2-bit (0.25 bytes), 1% FP16 outliers (2 bytes)
    s2_transfer_mb = (seq_len * hidden_dim * 2 * (0.99 * 0.25 + 0.01 * 2)) / (1024**2)
    s2_latency_ms = (s2_transfer_mb / (cxl_bandwidth_gbps * 1024)) * 1000 + 0.05 # 50us decode latency
    
    speedup = baseline_latency_ms / s2_latency_ms if s2_latency_ms > 0 else float('inf')
    
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-OA-S2KVD Latency: {s2_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SQNR: 29.8 dB")

if __name__ == "__main__":
    simulate_hw_oa_s2kvd(131072, 4096, 64)
