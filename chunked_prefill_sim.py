def simulate_chunked_prefill():
    print("=== Long Context Chunked Prefill Hardware Simulation ===")
    
    context_len = 128000 # 128K context
    chunk_size = 4096
    
    # Naive Prefill Memory (O(N^2))
    # Attention matrix memory for 128K context
    naive_attn_mem_gb = (context_len ** 2) * 2 / (1024**3)
    
    # Chunked Prefill Memory (O(N * C))
    chunked_attn_mem_gb = (context_len * chunk_size) * 2 / (1024**3)
    
    memory_reduction = naive_attn_mem_gb / chunked_attn_mem_gb
    
    print(f"Context Length: {context_len}")
    print(f"Naive Attention Memory: {naive_attn_mem_gb:.2f} GB")
    print(f"Chunked Attention Memory: {chunked_attn_mem_gb:.2f} GB")
    print(f"Memory Reduction: {memory_reduction:.2f}x")
    
if __name__ == "__main__":
    simulate_chunked_prefill()
