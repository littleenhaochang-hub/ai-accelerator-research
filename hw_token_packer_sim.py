import time

def simulate_hw_token_packer(sequence_length, sparsity):
    print(f"Simulating Hardware Token Packer for Dynamic Sparse Attention with {sequence_length} tokens and {sparsity*100}% sparsity...")
    active_tokens = int(sequence_length * (1 - sparsity))
    
    # Software gather/scatter latency
    sw_latency = sequence_length * 0.0005 + active_tokens * 0.001 
    
    # Hardware token packer latency (zero-cycle overhead during DMA)
    hw_latency = active_tokens * 0.0001 
    
    speedup = sw_latency / hw_latency
    
    print(f"SW Gather/Scatter Latency: {sw_latency:.4f} s")
    print(f"HW Token Packer Latency: {hw_latency:.4f} s")
    print(f"Speedup: {speedup:.2f}x")
    return speedup

simulate_hw_token_packer(65536, 0.90)
