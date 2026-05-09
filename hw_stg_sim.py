import numpy as np

def simulate_hw_stg(seq_len, dim, sparsity=0.9):
    print(f"Simulating Hardware Sparse Token Gatherer (HW-STG) - Seq: {seq_len}, Dim: {dim}, Sparsity: {sparsity}")
    
    # Software Gather: GPU threads read non-contiguous sparse indices
    # Severe penalty for uncoalesced memory access
    uncoalesced_bw = 200e9 # 200 GB/s effective bandwidth due to scatter/gather
    active_tokens = int(seq_len * (1 - sparsity))
    
    sw_latency = (active_tokens * dim * 2) / uncoalesced_bw * 1000 + 0.05 # + kernel launch
    
    # HW-STG: Inline DMA gatherer dynamically compacts sparse tokens into a continuous stream
    # before they hit the MAC array. Achieves near-peak bandwidth.
    coalesced_bw = 1000e9 # 1 TB/s effective bandwidth
    hw_latency = (active_tokens * dim * 2) / coalesced_bw * 1000
    
    print(f"Software Gather Latency: {sw_latency:.4f} ms")
    print(f"HW-STG Latency: {hw_latency:.4f} ms")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_stg(65536, 4096, 0.9)
