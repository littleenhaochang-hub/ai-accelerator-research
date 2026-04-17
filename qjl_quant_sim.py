import numpy as np

def simulate_qjl_quantization(dim=4096, tokens=1000, reduction_dim=1024):
    print("=== W4A4 QJL Quantization Simulation ===")
    print(f"Original Dim: {dim}, JL Reduction Dim: {reduction_dim}")
    
    # Original Data
    X = np.random.normal(0, 1, (tokens, dim))
    W = np.random.normal(0, 1, (dim, dim))
    
    # Baseline: Full Precision Matmul
    baseline_out = X @ W
    
    # QJL: Random projection matrix for Johnson-Lindenstrauss transform
    # Project to lower dimension before quantization
    R = np.random.normal(0, 1 / np.sqrt(reduction_dim), (dim, reduction_dim))
    
    # Projected features
    X_proj = X @ R
    W_proj = W.T @ R # Note: W.T for alignment
    
    # Naive INT4 Quantization on original
    X_scale = np.max(np.abs(X)) / 7.0
    W_scale = np.max(np.abs(W)) / 7.0
    X_q = np.round(X / X_scale) * X_scale
    W_q = np.round(W / W_scale) * W_scale
    naive_out = X_q @ W_q
    naive_mse = np.mean((baseline_out - naive_out)**2)
    
    # INT4 Quantization on QJL projected space
    X_proj_scale = np.max(np.abs(X_proj)) / 7.0
    W_proj_scale = np.max(np.abs(W_proj)) / 7.0
    X_proj_q = np.round(X_proj / X_proj_scale) * X_proj_scale
    W_proj_q = np.round(W_proj / W_proj_scale) * W_proj_scale
    
    # Reconstruct inner products in projected space
    qjl_out = X_proj_q @ W_proj_q.T
    qjl_mse = np.mean((baseline_out - qjl_out)**2)
    
    sqnr_naive = 10 * np.log10(np.mean(baseline_out**2) / naive_mse)
    sqnr_qjl = 10 * np.log10(np.mean(baseline_out**2) / qjl_mse)
    
    print(f"Naive INT4 Matmul SQNR: {sqnr_naive:.2f} dB")
    print(f"QJL INT4 Matmul SQNR: {sqnr_qjl:.2f} dB")
    
    # Note: QJL reduces MAC operations by (dim / reduction_dim) but adds projection overhead.
    # In hardware, R can be a sparse random matrix (e.g. +1, -1, 0) removing multiplication.
    mac_reduction = dim / reduction_dim
    print(f"MAC Operation Reduction (Speedup Bound): {mac_reduction:.2f}x")

if __name__ == "__main__":
    simulate_qjl_quantization()
