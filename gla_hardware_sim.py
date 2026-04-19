import math

def simulate_gla_hardware():
    # Context: Gated Linear Attention (GLA) vs Softmax Attention
    # Softmax Attention needs to store KV cache for the entire sequence.
    # GLA compresses historical context into a fixed-size hidden state (like RNN/Mamba)
    # via hardware-friendly data-dependent gating and associative scans.
    
    seq_len = 8192
    head_dim = 128
    num_heads = 32
    
    # Softmax Attention KV Cache (FP16)
    # Size: seq_len * num_heads * head_dim * 2 (K and V) * 2 bytes
    softmax_kv_mb = (seq_len * num_heads * head_dim * 2 * 2) / (1024**2)
    
    # GLA Fixed-size State Cache (FP16)
    # State is head_dim x head_dim matrix per head.
    # Size: num_heads * (head_dim * head_dim) * 2 bytes
    gla_state_mb = (num_heads * head_dim * head_dim * 2) / (1024**2)
    
    # Compute: 
    # Softmax requires O(N^2) dot products per token in prefill, O(N) per token in generation.
    # GLA requires O(N) via associative parallel scan in prefill, O(1) per token in generation.
    softmax_gen_macs_per_token = seq_len * num_heads * head_dim * 2
    gla_gen_macs_per_token = num_heads * (head_dim * head_dim) * 2
    
    print("--- Gated Linear Attention (GLA) Hardware Simulation ---")
    print(f"Softmax Attention KV Cache: {softmax_kv_mb:.2f} MB")
    print(f"GLA Fixed State Cache: {gla_state_mb:.2f} MB")
    print(f"Memory Reduction: {softmax_kv_mb / gla_state_mb:.2f}x")
    print(f"Softmax Generation MACs (Token N=8192): {softmax_gen_macs_per_token:.2e}")
    print(f"GLA Generation MACs (Token N=8192): {gla_gen_macs_per_token:.2e}")
    print(f"Compute Speedup (Generation): {softmax_gen_macs_per_token / gla_gen_macs_per_token:.2f}x")
    print("Conclusion: GLA replaces the infinitely growing KV Cache with a fixed-size state matrix, achieving massive memory and compute reductions for long contexts. Hardware should implement 'Associative Scan ALUs' natively.")

if __name__ == "__main__":
    simulate_gla_hardware()
