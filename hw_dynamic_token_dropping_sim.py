import numpy as np

def simulate_hardware_dynamic_token_dropping(seq_len, dim, layers=32, drop_ratio=0.5):
    print(f"Simulating Hardware Dynamic Token Dropping Engine (HW-DTDE) - Seq: {seq_len}, Dim: {dim}")
    
    # Standard MACs
    mac_ops_per_layer = seq_len * dim * dim * 4
    total_standard_macs = mac_ops_per_layer * layers
    
    # Dropped MACs
    # Token drops progressively across layers
    active_tokens = seq_len
    total_dropped_macs = 0
    for i in range(layers):
        total_dropped_macs += active_tokens * dim * dim * 4
        # Assume linear dropping down to (1-drop_ratio)
        drop_factor = 1 - (drop_ratio * (i / layers))
        active_tokens = int(seq_len * drop_factor)
        
    print(f"Standard Total MACs: {total_standard_macs / 1e12:.2f} T-MACs")
    print(f"Hardware Dropped Total MACs: {total_dropped_macs / 1e12:.2f} T-MACs")
    print(f"Compute Reduction: {100 - (total_dropped_macs / total_standard_macs * 100):.2f}%")
    print(f"Speedup: {total_standard_macs / total_dropped_macs:.2f}x")
    return total_standard_macs, total_dropped_macs

if __name__ == "__main__":
    simulate_hardware_dynamic_token_dropping(8192, 4096, 32, 0.7)
