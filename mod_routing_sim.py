import numpy as np

def simulate_mod_hardware():
    print("Starting Mixture-of-Depths (MoD) Hardware Routing Simulation...")
    
    seq_len = 8192
    num_layers = 32
    dim = 4096
    
    # Baseline: Compute all tokens at all layers
    # Tokens * Layers * (FFN + Attention roughly approximated as MACs per token)
    baseline_macs_per_layer = seq_len * (dim * dim * 2) # simplified
    baseline_total_macs = baseline_macs_per_layer * num_layers
    
    # Mixture-of-Depths (MoD)
    # Only top-k tokens participate in self-attention and FFN at specific layers.
    # Say 50% capacity factor (k = seq_len // 2) at every alternating layer.
    
    capacity_factor = 0.5
    layers_with_mod = num_layers // 2
    layers_dense = num_layers - layers_with_mod
    
    active_tokens_per_mod_layer = int(seq_len * capacity_factor)
    
    # Compute MACs
    dense_macs = layers_dense * baseline_macs_per_layer
    mod_macs = layers_with_mod * (active_tokens_per_mod_layer * (dim * dim * 2))
    total_mod_macs = dense_macs + mod_macs
    
    compute_reduction = (1 - total_mod_macs / baseline_total_macs) * 100
    
    # Hardware overhead: Token Router
    # Routing requires computing a scalar weight per token and sorting/Top-K.
    # Latency penalty if sorting is done in software.
    print(f"Context Length: {seq_len}, Total Layers: {num_layers}")
    print(f"MoD Capacity Factor: {capacity_factor*100:.1f}%, Applied to {layers_with_mod} layers")
    print(f"Baseline Compute MACs: {baseline_total_macs / 1e9:.2f} G-MACs")
    print(f"MoD Compute MACs: {total_mod_macs / 1e9:.2f} G-MACs")
    print(f"Compute Energy Reduction: {compute_reduction:.2f}%")
    print("Conclusion: MoD achieves significant compute reduction by routing tokens around layers. Hardware requires a 'Token Bypasser & Router' logic inside the inter-layer SRAM buffer to skip inactive tokens dynamically without fragmenting memory.")

if __name__ == "__main__":
    simulate_mod_hardware()