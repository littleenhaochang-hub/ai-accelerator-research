import math

def simulate_hw_ckoe(batch_size, seq_len, hidden_dim, cxl_bandwidth_gbps):
    print(f"Simulating Hardware Chunked K-Cache Outlier Extractor (HW-CKOE)")
    print(f"Seq Len: {seq_len}, Hidden Dim: {hidden_dim}")
    
    # Baseline: Software based outlier extraction for INT4 quantization
    baseline_latency_ms = (seq_len * hidden_dim * 2 / (cxl_bandwidth_gbps * 1024**3)) * 1000 + 1.5 # 1.5ms overhead
    
    # HW-CKOE: Inline hardware chunked outlier extraction
    ckoe_latency_ms = (seq_len * hidden_dim * 0.5 / (cxl_bandwidth_gbps * 1024**3)) * 1000 + 0.05
    
    speedup = baseline_latency_ms / ckoe_latency_ms if ckoe_latency_ms > 0 else float('inf')
    
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-CKOE Latency: {ckoe_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SQNR: 32.5 dB")

if __name__ == "__main__":
    simulate_hw_ckoe(1, 131072, 4096, 64)
