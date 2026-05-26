import time

def simulate_hw_sparse_moe_prefetch(experts=1024, sparsity=0.9):
    # Baseline: CPU manages sparse fetching, high software overhead for calculating which chunks are needed
    software_latency_ms = experts * 0.02
    
    # Proposed: Hardware Sparse MoE Chunk Prefetcher (HW-SMC-PF)
    # Hardware autonomously masks out 90% of expert chunks based on predictor and fetches the rest via DMA
    hardware_latency_ms = experts * (1 - sparsity) * 0.005 + 0.002
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Total Experts: {experts}, Chunk Sparsity: {sparsity*100}%")
    print(f"Baseline Latency (Software Tracking): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SMC-PF): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_sparse_moe_prefetch()
