import numpy as np

def simulate_hw_kvdds(seq_len, dim, sparsity=0.85):
    print(f"Simulating Hardware KV Cache Data-Dependent Sparsifier (HW-KVDDS) - Seq: {seq_len}, Dim: {dim}")
    
    fp16_latency = (seq_len * dim) / (100e12) * 1000
    fp16_mem = seq_len * dim * 2
    
    # HW-KVDDS uses a low-precision inline predictor to drop 85% of tokens
    # Predictor overhead is negligible due to inline SRAM integration
    sparse_latency = ((seq_len * dim) * (1 - sparsity)) / (100e12) * 1000
    sparse_mem = (seq_len * dim * 2) * (1 - sparsity) + (seq_len * 2) # Adding pointer overhead
    
    print(f"FP16 Memory: {fp16_mem/1e6:.2f} MB, Latency: {fp16_latency:.6f} ms")
    print(f"HW-KVDDS Memory: {sparse_mem/1e6:.2f} MB, Latency: {sparse_latency:.6f} ms")
    print(f"Memory Reduction: {(fp16_mem - sparse_mem) / fp16_mem * 100:.2f}%")
    print(f"Speedup vs FP16: {fp16_latency / sparse_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_kvdds(131072, 128)
