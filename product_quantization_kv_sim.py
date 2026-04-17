import numpy as np

def simulate_pq_kv_cache():
    print("Starting Product Quantization KV Cache Hardware Simulation...")
    
    seq_len = 16384
    dim = 4096
    
    # Baseline: 16-bit (2 bytes) per element
    baseline_memory_bytes = seq_len * dim * 2
    
    # PQ Compression:
    # Split dimension into subvectors. e.g., 32 subvectors of length 128
    num_subvectors = 32
    subvector_len = dim // num_subvectors
    
    # Codebook size: 256 centroids per subvector (1 byte index)
    codebook_size = 256
    index_bits = 8
    
    # PQ memory:
    # 1 byte per subvector per token
    pq_indices_bytes = seq_len * num_subvectors * 1
    # Codebooks: 32 * 256 * 128 * 2 bytes = 2MB (shared across tokens)
    codebook_bytes = num_subvectors * codebook_size * subvector_len * 2
    
    total_pq_memory_bytes = pq_indices_bytes + codebook_bytes
    
    memory_reduction_ratio = baseline_memory_bytes / total_pq_memory_bytes
    
    # Simulate fetch latency (simplified)
    bandwidth_GBps = 100
    baseline_latency_ms = (baseline_memory_bytes / 1e9) / bandwidth_GBps * 1000
    pq_latency_ms = (total_pq_memory_bytes / 1e9) / bandwidth_GBps * 1000
    
    lut_latency_penalty_ms = (seq_len * num_subvectors) / 1e8 * 1000 
    
    total_pq_time = pq_latency_ms + lut_latency_penalty_ms
    speedup = baseline_latency_ms / total_pq_time
    
    print(f"Baseline KV Cache Memory: {baseline_memory_bytes / 1e6:.2f} MB")
    print(f"PQ KV Cache Memory: {total_pq_memory_bytes / 1e6:.2f} MB")
    print(f"Memory Footprint Reduction: {(1 - total_pq_memory_bytes/baseline_memory_bytes)*100:.2f}%")
    print(f"Effective Bandwidth Speedup: {speedup:.2f}x")
    print("Conclusion: PQ drastically reduces KV cache memory but requires integrated SRAM LUT arrays to decompress on-the-fly without adding latency.")

if __name__ == "__main__":
    simulate_pq_kv_cache()
