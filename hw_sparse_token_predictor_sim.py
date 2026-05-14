import time
import random

def simulate_dense_ffn(seq_len, hidden_dim):
    # O(N * D) time complexity
    macs = seq_len * hidden_dim
    return macs / 1e10 # baseline time

def simulate_sparse_predictor_ffn(seq_len, hidden_dim, sparsity=0.85):
    # Predictor overhead + sparse execution
    predictor_overhead = (seq_len * 64) / 1e11 # Lightweight INT2 predictor
    dense_macs = seq_len * hidden_dim * (1 - sparsity)
    execution_time = dense_macs / 1e10
    return predictor_overhead + execution_time

if __name__ == "__main__":
    seq_len = 32768
    hidden_dim = 14336 # e.g. Llama FFN
    
    dense_time = simulate_dense_ffn(seq_len, hidden_dim)
    sparse_time = simulate_sparse_predictor_ffn(seq_len, hidden_dim)
    
    print(f"Dense FFN Latency: {dense_time:.4f} s")
    print(f"HW-Sparse-Predictor Latency: {sparse_time:.4f} s")
    print(f"Speedup: {dense_time / sparse_time:.2f}x")
