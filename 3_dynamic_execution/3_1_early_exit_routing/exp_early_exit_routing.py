import torch
import torch.nn as nn
import time

class DummyTransformerLayer(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model)
        )
        self.norm = nn.LayerNorm(d_model)
        
    def forward(self, x):
        return self.norm(x + self.ffn(x))

def run_early_exit_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, d_model = 1, 2048, 512
    num_layers = 16
    
    print(f"Initializing Token-Level Early-Exit Experiment (Dynamic Routing)")
    print(f"Seq: {seq_len}, Dim: {d_model}, Layers: {num_layers}")
    
    # Generate initial embeddings
    x = torch.randn(batch_size, seq_len, d_model)
    
    layers = nn.ModuleList([DummyTransformerLayer(d_model) for _ in range(num_layers)])
    
    # --- Standard Execution (All Layers) ---
    t0 = time.time()
    out_standard = x.clone()
    for layer in layers:
        out_standard = layer(out_standard)
    t_standard = time.time() - t0
    
    # --- Early-Exit Execution ---
    # In a real model, an internal classifier/confidence-scorer decides 
    # if a token's representation is "stable" enough to stop computing.
    # We simulate this by stopping computation for 80% of tokens at layer 8.
    
    t0 = time.time()
    out_dynamic = x.clone()
    active_tokens = torch.ones(seq_len, dtype=torch.bool)
    exit_layer_threshold = 8
    
    # We will pretend that at layer 8, 80% of tokens are "easy" (e.g., "the", "a", punctuation)
    # and don't need deeper semantic processing.
    num_easy_tokens = int(0.8 * seq_len)
    easy_indices = torch.randperm(seq_len)[:num_easy_tokens]
    
    for i, layer in enumerate(layers):
        if i == exit_layer_threshold:
            # 80% of tokens exit the pipeline
            active_tokens[easy_indices] = False
            
        # Only process active tokens to save FLOPs
        if not active_tokens.any():
            break
            
        active_indices = active_tokens.nonzero(as_tuple=True)[0]
        # Gather active tokens
        active_x = out_dynamic[:, active_indices, :]
        
        # Forward pass on active subset
        out_active = layer(active_x)
        
        # Scatter back
        out_dynamic[:, active_indices, :] = out_active
        
    t_dynamic = time.time() - t0
    
    print(f"\n--- Execution Latency ---")
    print(f"1. Standard Dense (All Layers) : {t_standard:.4f}s")
    print(f"2. Early-Exit Sparse Routing   : {t_dynamic:.4f}s")
    print(f"-> Latency Reduction           : {(1 - t_dynamic/t_standard)*100:.2f}%")
    
    print("\n[CHALLENGE RECORDED]:")
    print("While early-exiting saves FLOPs mathematically, the PyTorch gather/scatter operations")
    print("(boolean masking and indexing) introduce severe memory bandwidth overhead.")
    print("On GPUs and Edge NPUs, reading sparse token indices from memory is often slower")
    print("than just executing the dense matrix multiplication for all tokens. ")

if __name__ == "__main__":
    run_early_exit_experiment()
