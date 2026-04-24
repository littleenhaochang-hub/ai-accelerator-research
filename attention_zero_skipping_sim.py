import time

def dense_attention_compute(seq_len, d_model):
    # Simulated latency for standard O(N^2) dense attention MACs
    macs = seq_len * seq_len * d_model
    latency = macs * 1e-9  # arbitrary scale for ns per MAC
    return latency

def zero_skipped_attention_compute(seq_len, d_model, sparsity_ratio=0.85):
    # Simulated latency using a lightweight predictor + sparse MAC execution
    # Predictor overhead is O(N^2 * reduced_d)
    predictor_macs = seq_len * seq_len * (d_model // 16)
    predictor_latency = predictor_macs * 1e-9
    
    # Only compute full dot products for the top 15% (1 - sparsity_ratio)
    sparse_macs = seq_len * seq_len * d_model * (1.0 - sparsity_ratio)
    sparse_latency = sparse_macs * 1e-9
    
    return predictor_latency + sparse_latency

def main():
    seq_len = 8192
    d_model = 128
    
    print("Running Attention Zero-Skipping Hardware Simulation...")
    dense_lat = dense_attention_compute(seq_len, d_model)
    print(f"Dense Attention Latency: {dense_lat:.4f} s")
    
    zvs_lat = zero_skipped_attention_compute(seq_len, d_model)
    print(f"Zero-Skipped Attention Latency: {zvs_lat:.4f} s")
    
    speedup = dense_lat / zvs_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
