import time

def simulate_dense_mla_up_projection(latent_dim, up_dim, seq_len):
    # O(N * D_latent * D_up)
    macs = seq_len * latent_dim * up_dim
    return macs / 1e10 # Assume 10 TFLOPs effective

def simulate_sparse_mla_up_projection(latent_dim, up_dim, seq_len, sparsity=0.75):
    # Skip zero/near-zero latent dimensions in hardware
    dense_macs = seq_len * latent_dim * up_dim * (1 - sparsity)
    hardware_overhead = (seq_len * latent_dim) / 1e11 
    return (dense_macs / 1e10) + hardware_overhead

if __name__ == "__main__":
    latent_dim = 512
    up_dim = 2048 # e.g. DeepSeek MLA Key/Value projection
    seq_len = 8192
    
    dense_time = simulate_dense_mla_up_projection(latent_dim, up_dim, seq_len)
    sparse_time = simulate_sparse_mla_up_projection(latent_dim, up_dim, seq_len)
    
    print(f"Dense MLA Up-Projection Latency: {dense_time:.4f} s")
    print(f"HW-SMLU Sparse Latency: {sparse_time:.4f} s")
    print(f"Speedup: {dense_time / sparse_time:.2f}x")
