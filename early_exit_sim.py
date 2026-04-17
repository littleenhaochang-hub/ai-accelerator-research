import numpy as np

def simulate_early_exit(seq_len=2048, total_layers=32, exit_layer=16, easy_token_ratio=0.6):
    print("=== Early-Exit Dynamic Depth Hardware Simulation ===")
    
    # Baseline: All tokens pass through all layers
    # Abstract compute unit = 1 token processing 1 layer
    baseline_compute_units = seq_len * total_layers
    
    # Proposed: Easy tokens exit early, hard tokens go through all layers
    # Hardware implements a lightweight confidence router at the exit_layer
    hard_tokens = int(seq_len * (1 - easy_token_ratio))
    easy_tokens = seq_len - hard_tokens
    
    proposed_compute_units = (easy_tokens * exit_layer) + (hard_tokens * total_layers)
    
    speedup = baseline_compute_units / proposed_compute_units
    energy_reduction = 1.0 - (proposed_compute_units / baseline_compute_units)
    
    print(f"[Baseline] Total Layer-Tokens Processed: {baseline_compute_units}")
    print(f"[Proposed] Dynamic Layer-Tokens Processed: {proposed_compute_units}")
    print(f"Hardware Throughput Speedup: {speedup:.2f}x")
    print(f"Energy Reduction: {energy_reduction*100:.2f}%")

if __name__ == "__main__":
    simulate_early_exit()
