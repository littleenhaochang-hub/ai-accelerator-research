import math

def simulate_token_merging():
    # Context: 4096 tokens, dropping/merging r tokens per layer
    initial_tokens = 4096
    num_layers = 32
    merge_rate_per_layer = 64 # tokens merged per layer
    head_dim = 128
    num_heads = 32
    
    mac_ops_baseline = 0
    mac_ops_tome = 0
    
    current_tokens = initial_tokens
    
    for layer in range(num_layers):
        # Attention MACs roughly 2 * N^2 * D
        attn_macs_baseline = 2 * (initial_tokens**2) * (head_dim * num_heads)
        attn_macs_tome = 2 * (current_tokens**2) * (head_dim * num_heads)
        
        mac_ops_baseline += attn_macs_baseline
        mac_ops_tome += attn_macs_tome
        
        # Merge tokens
        current_tokens = max(128, current_tokens - merge_rate_per_layer)
        
    speedup = mac_ops_baseline / mac_ops_tome
    
    # Hardware overhead: Bipartite matching for similarity (cosine sim)
    # Roughly N^2 / 2 comparisons per layer
    
    print("--- Token Merging (ToMe) Hardware Simulation ---")
    print(f"Baseline Attention MACs: {mac_ops_baseline:.2e}")
    print(f"ToMe Attention MACs: {mac_ops_tome:.2e}")
    print(f"Compute Speedup: {speedup:.2f}x")
    print(f"Final Token Count at Layer {num_layers}: {current_tokens}")
    print("Conclusion: Significant MAC reduction, but bipartite matching requires dedicated hardware Euclidean/Cosine distance engines.")

if __name__ == "__main__":
    simulate_token_merging()
