def simulate_sparse_attention():
    print("=== Sparse Attention Hardware Pre-Filtering ===")
    
    # Dense Attention MACs (e.g. 16K context)
    dense_macs = 16384 ** 2
    
    # Hardware Pre-filtering (Predicting top-K chunks)
    sparsity_ratio = 0.1 # 10% density
    sparse_macs = dense_macs * sparsity_ratio
    
    # Hardware overhead for predictor (e.g. 5%)
    predictor_overhead = dense_macs * 0.05
    
    total_sparse_macs = sparse_macs + predictor_overhead
    
    mac_reduction = dense_macs / total_sparse_macs
    
    print(f"Dense MACs: {dense_macs}")
    print(f"Total Sparse MACs (inc. overhead): {total_sparse_macs}")
    print(f"Compute Reduction: {mac_reduction:.2f}x")
    
if __name__ == "__main__":
    simulate_sparse_attention()
