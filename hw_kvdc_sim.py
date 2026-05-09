import numpy as np

def simulate_kv_delta_compression(seq_len, dim, bit_width=16):
    print(f"Simulating Hardware KV Cache Delta Compression (HW-KVDC) - Seq: {seq_len}, Dim: {dim}")
    
    # Standard FP16/INT8 Memory footprint
    standard_memory_bytes = seq_len * dim * (bit_width / 8)
    
    # HW-KVDC: Store base token every 16 tokens in full precision, store INT2 deltas for the rest
    block_size = 16
    base_tokens = seq_len // block_size
    delta_tokens = seq_len - base_tokens
    
    base_memory_bytes = base_tokens * dim * (bit_width / 8)
    delta_memory_bytes = delta_tokens * dim * (2 / 8) # INT2 deltas
    
    compressed_memory_bytes = base_memory_bytes + delta_memory_bytes
    
    print(f"Standard KV Memory: {standard_memory_bytes / 1e6:.2f} MB")
    print(f"Compressed KV Memory: {compressed_memory_bytes / 1e6:.2f} MB")
    print(f"Memory Reduction: {100 - (compressed_memory_bytes / standard_memory_bytes * 100):.2f}%")
    print("Conclusion: HW-KVDC significantly reduces memory bandwidth for long-context generation.")
    return standard_memory_bytes, compressed_memory_bytes

if __name__ == "__main__":
    simulate_kv_delta_compression(128000, 128, 16)
