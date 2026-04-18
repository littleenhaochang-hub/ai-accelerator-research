import math

def simulate_activation_sparsity():
    # Context: 4096 tokens, FFN layer
    # SwiGLU / ReLU activations naturally have high sparsity (e.g., 60% zeros)
    
    tokens = 4096
    hidden_dim = 4096
    ffn_dim = 14336  # e.g., Llama 2 7B
    sparsity_ratio = 0.60 # 60% of activations are zero after SiLU/ReLU
    
    # Baseline Dense MACs for Down-Projection (FFN)
    # MACs = tokens * ffn_dim * hidden_dim
    dense_macs = tokens * ffn_dim * hidden_dim
    
    # Sparse MACs
    # In hardware, zero-skipping means we don't compute MAC if activation is zero
    sparse_macs = dense_macs * (1.0 - sparsity_ratio)
    
    # Hardware overhead: Zero-Value Predictor / Compressor
    # Need a bitmask to indicate non-zero values
    bitmask_size_mb = (tokens * ffn_dim) / 8 / (1024**2)
    
    speedup = dense_macs / sparse_macs
    
    print("--- Activation Sparsity (Zero-Skipping) Hardware Simulation ---")
    print(f"Dense Down-Projection MACs: {dense_macs:.2e}")
    print(f"Sparse Down-Projection MACs: {sparse_macs:.2e}")
    print(f"Compute Speedup: {speedup:.2f}x")
    print(f"Bitmask Overhead: {bitmask_size_mb:.2f} MB")
    print("Conclusion: Activation sparsity provides massive compute savings but requires an 'Asynchronous Zero-Skipping Controller' to avoid pipeline bubbles when branching.")

if __name__ == "__main__":
    simulate_activation_sparsity()
