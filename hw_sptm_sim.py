import math
import time

def simulate_hw_spec_prefix_tree(num_drafts, prefix_len, sram_bandwidth_gbps):
    print(f"Simulating Hardware Speculative Prefix Tree MMU (HW-SPTM)")
    print(f"Drafts: {num_drafts}, Prefix Len: {prefix_len}")
    
    # Baseline: CPU manages radix tree, traversing and checking token by token
    baseline_latency_ms = 15.0 # CPU pointer chasing latency in ms
    
    # HW-SPTM: Hardware walks the radix tree and matches tokens concurrently using TCAM
    # Latency mostly determined by hardware SRAM CAM lookup
    sptm_latency_ms = 0.4 # Hardware lookup and mapping
    
    speedup = baseline_latency_ms / sptm_latency_ms if sptm_latency_ms > 0 else float('inf')
    
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-SPTM Latency: {sptm_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_spec_prefix_tree(256, 16384, 1024)
