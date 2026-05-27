import time
import math
import random

class HW_MoE_SpecTrajPrefetcher:
    def __init__(self, num_experts=128, dim=1024):
        self.num_experts = num_experts
        self.dim = dim
        self.dma_bandwidth = 64 * 1024**3  # 64 GB/s PCIe Gen4
        self.expert_size = (dim * dim * 2) * 2  # ~4MB per expert
        
    def simulate_baseline_fetch(self, batch_size):
        # Demand fetch: Wait for routing, then fetch
        fetch_bytes = batch_size * self.expert_size
        latency = fetch_bytes / self.dma_bandwidth
        return latency

    def simulate_prefetch(self, batch_size):
        # Assuming 85% accuracy in trajectory prediction
        accuracy = 0.85
        hits = int(batch_size * accuracy)
        misses = batch_size - hits
        
        # Only pay penalty for misses
        miss_bytes = misses * self.expert_size
        latency = miss_bytes / self.dma_bandwidth
        
        return latency, hits, misses

def run_sim():
    print("Running Hardware MoE Speculative Trajectory Prefetcher (HW-MSTP) Simulation...")
    sim = HW_MoE_SpecTrajPrefetcher()
    
    seq_len = 128
    
    baseline_latency = sim.simulate_baseline_fetch(seq_len)
    prefetch_latency, hits, misses = sim.simulate_prefetch(seq_len)
    
    speedup = baseline_latency / prefetch_latency if prefetch_latency > 0 else float('inf')
    
    print(f"Baseline Demand Fetch Latency: {baseline_latency * 1000:.2f} ms")
    print(f"HW-MSTP Prefetch Latency: {prefetch_latency * 1000:.2f} ms")
    print(f"Predictor Hits: {hits}, Misses: {misses}")
    print(f"Speedup: {speedup:.2f}x")
    
if __name__ == '__main__':
    run_sim()
