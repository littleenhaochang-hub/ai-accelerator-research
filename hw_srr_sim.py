import time

def simulate_software_rag_filtering(num_chunks, hidden_dim):
    # O(C * D) dense similarity calculation + sorting
    latency = (num_chunks * hidden_dim) / 1e9 + 0.015
    return latency

def simulate_hw_srr_filtering(num_chunks, hidden_dim):
    # Hardware Semantic RAG Router: Parallel SRAM CAM + Adder Trees
    latency = (num_chunks * hidden_dim) / 1e11 + 0.0005
    return latency

if __name__ == "__main__":
    num_chunks = 8192 # Large RAG context database
    hidden_dim = 1024 # Embedding dimension
    
    soft_time = simulate_software_rag_filtering(num_chunks, hidden_dim)
    hw_time = simulate_hw_srr_filtering(num_chunks, hidden_dim)
    
    print(f"Software RAG Filtering Latency: {soft_time:.4f} s")
    print(f"HW-SRR Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
