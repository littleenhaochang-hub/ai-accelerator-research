import numpy as np

def simulate_nm_structured_sparsity(dim=4096, n=2, m=4):
    print(f"=== {n}:{m} Structured Sparsity Hardware Simulation ===")
    
    # Baseline Dense MACs
    baseline_macs = dim * dim
    
    # Proposed N:M Sparsity
    # For every M elements, only N are non-zero.
    sparsity_ratio = (m - n) / m
    proposed_macs = baseline_macs * (1 - sparsity_ratio)
    
    # Hardware metadata overhead (indices for the non-zero elements)
    # E.g., for 2:4, need 2 bits per element in the block to store index (for M=4, log2(4)=2 bits)
    index_bits_per_block = np.ceil(np.log2(m)) * n
    metadata_overhead_bits = (dim * dim / m) * index_bits_per_block
    
    speedup = baseline_macs / proposed_macs
    
    print(f"[Baseline] Dense MACs: {baseline_macs}")
    print(f"[Proposed] {n}:{m} Sparse MACs: {int(proposed_macs)}")
    print(f"Compute Speedup: {speedup:.2f}x")
    print(f"Metadata Overhead (for 4Kx4K layer): {metadata_overhead_bits / (8 * 1024):.2f} KB")

if __name__ == "__main__":
    simulate_nm_structured_sparsity()
