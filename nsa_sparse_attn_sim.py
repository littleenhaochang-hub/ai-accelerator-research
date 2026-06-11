import time
import random
import math

def simulate_full_attention(seq_len, block_size):
    start = time.time()
    num_blocks = seq_len // block_size
    # O(N^2) full attention
    for i in range(num_blocks):
        for j in range(num_blocks):
            # Dense dot product
            _ = random.random() * random.random()
            # Memory latency
            time.sleep(0.00005)
    end = time.time()
    return end - start

def simulate_nsa_sparse_attention(seq_len, block_size, compression_ratio, selection_ratio):
    # NSA: Natively trainable Sparse Attention
    # Combines coarse-grained token compression with fine-grained token selection
    # Hardware-aligned to balance arithmetic intensity
    start = time.time()
    
    num_blocks = seq_len // block_size
    
    # Coarse-grained compressed context processing
    compressed_blocks = int(num_blocks * compression_ratio)
    for i in range(num_blocks):
        for j in range(compressed_blocks):
            _ = random.random() * random.random()
            time.sleep(0.00005)
            
    # Fine-grained token selection (hardware-aligned sparse pattern)
    selected_blocks = int(num_blocks * selection_ratio)
    for i in range(num_blocks):
        for j in range(selected_blocks):
            # Optimized memory layout assumes contiguous block fetching in HW
            _ = random.random() * random.random()
            time.sleep(0.00001) # Reduced latency due to hardware-aligned fetches
            
    end = time.time()
    return end - start

if __name__ == "__main__":
    seq = 32768 # 32K context
    block = 128
    
    # Using parameters inspired by NSA
    c_ratio = 0.125
    s_ratio = 0.125
    
    full_time = simulate_full_attention(seq, block)
    nsa_time = simulate_nsa_sparse_attention(seq, block, c_ratio, s_ratio)
    
    speedup = full_time / nsa_time if nsa_time > 0 else float('inf')
    
    print(f"Full Attention Latency: {full_time*1000:.2f} ms")
    print(f"NSA (Native Sparse Attention) Latency: {nsa_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
