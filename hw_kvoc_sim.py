import numpy as np

def simulate_hw_kvoc(seq_len, dim, outlier_ratio=0.01):
    print(f"Simulating Hardware KV Cache Outlier Compensator (HW-KVOC) - Seq: {seq_len}, Dim: {dim}")
    
    # Standard FP16
    fp16_mem = seq_len * dim * 2
    fp16_latency = (seq_len * dim) / (100e12) * 1000
    
    # HW-KVOC (99% INT4 + 1% FP16 Outliers)
    # Dense INT4 matrix
    int4_mem = seq_len * dim * 0.5
    int4_latency = (seq_len * dim) / (400e12) * 1000 # 4x throughput for INT4
    
    # Sparse FP16 Outliers (Stored in dedicated TCAM/SRAM to avoid fragmentation)
    outlier_mem = (seq_len * dim * outlier_ratio * 2) + (seq_len * dim * outlier_ratio * 2) # value + index
    outlier_latency = (seq_len * dim * outlier_ratio) / (100e12) * 1000
    
    # Parallel execution in HW: latency is max of both paths
    kvoc_mem = int4_mem + outlier_mem
    kvoc_latency = max(int4_latency, outlier_latency)
    
    print(f"FP16 Memory: {fp16_mem/1e6:.2f} MB, Latency: {fp16_latency:.6f} ms")
    print(f"HW-KVOC Memory: {kvoc_mem/1e6:.2f} MB, Latency: {kvoc_latency:.6f} ms")
    print(f"Memory Reduction: {(fp16_mem - kvoc_mem) / fp16_mem * 100:.2f}%")
    print(f"Speedup vs FP16: {fp16_latency / kvoc_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_kvoc(128000, 128)
