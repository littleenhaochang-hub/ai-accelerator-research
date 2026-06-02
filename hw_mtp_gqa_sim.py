import math

def simulate_hw_mtp_gqa(query_groups, seq_len, head_dim, num_drafts, sram_bandwidth_gbps):
    print(f"Simulating Hardware MTP GQA Broadcaster (HW-MTP-GQA)")
    print(f"Query Groups: {query_groups}, Drafts: {num_drafts}")
    
    # Baseline: CPU/NPU reads shared KV cache for each MTP draft branch independently
    baseline_transfer_mb = (query_groups * num_drafts * seq_len * head_dim * 2 * 2) / (1024**2)
    baseline_latency_ms = (baseline_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 1.0 # 1ms setup
    
    # HW-MTP-GQA: Hardware broadcasts shared KV to all draft MACs in zero cycles
    mtp_gqa_transfer_mb = (query_groups * seq_len * head_dim * 2 * 2) / (1024**2)
    mtp_gqa_latency_ms = (mtp_gqa_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.1 # 0.1ms HW delay
    
    speedup = baseline_latency_ms / mtp_gqa_latency_ms if mtp_gqa_latency_ms > 0 else float('inf')
    
    print(f"Baseline Transfer: {baseline_transfer_mb:.2f} MB")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-MTP-GQA Transfer: {mtp_gqa_transfer_mb:.2f} MB")
    print(f"HW-MTP-GQA Latency: {mtp_gqa_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_mtp_gqa(8, 32768, 128, 4, 1024)
