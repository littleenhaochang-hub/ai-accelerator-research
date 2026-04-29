import time
import random

def simulate_baseline_moe_transfer():
    print("Simulating Baseline CPU-GPU MoE Expert Fetching...")
    transfer_latency = 0
    for _ in range(100):
        # CPU to GPU bounce buffer overhead
        transfer_latency += random.uniform(1.5, 2.5) 
    return transfer_latency

def simulate_p2p_ring_dma_moe():
    print("Simulating MoE P2P Ring DMA Transfer...")
    transfer_latency = 0
    for _ in range(100):
        # Direct NVMe to GPU/NPU via P2P Ring DMA
        transfer_latency += random.uniform(0.3, 0.6)
    return transfer_latency

baseline = simulate_baseline_moe_transfer()
proposed = simulate_p2p_ring_dma_moe()
speedup = baseline / proposed

print(f"Baseline Latency: {baseline:.2f} ms")
print(f"Proposed P2P Ring DMA Latency: {proposed:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
