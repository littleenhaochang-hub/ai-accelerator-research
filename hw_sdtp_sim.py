import time

def simulate_hw_sdtp(draft_tokens=64, target_layer_size_mb=120):
    # Baseline: CPU requests target model weights from DRAM *after* draft generation completes
    software_latency_ms = (target_layer_size_mb / 64) * 10 # 64 GB/s memory bandwidth assumption
    
    # Proposed: Hardware Speculative Draft Target Prefetcher (HW-SDTP)
    # Starts DMA fetching target weights asynchronously during the last few draft token generations
    hardware_latency_ms = (target_layer_size_mb / 64) * 10 * 0.1 # 90% latency hidden
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Draft Tokens: {draft_tokens}, Target Layer Size: {target_layer_size_mb} MB")
    print(f"Baseline Latency (Demand Fetch): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SDTP): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_sdtp()
