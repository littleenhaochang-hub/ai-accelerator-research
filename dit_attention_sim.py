import numpy as np

def simulate_dit_adaptive_attention(image_size=1024, patch_size=16, sram_capacity_mb=2):
    print("=== DiT Adaptive Global-Local Attention Hardware Simulation ===")
    
    # Calculate sequence length for DiT
    seq_len = (image_size // patch_size) ** 2 # 64x64 = 4096 patches
    print(f"Sequence Length (Patches): {seq_len}")
    
    # Baseline: Full Global Attention (O(N^2) memory and compute)
    baseline_compute = seq_len * seq_len
    # Memory footprint size roughly proportional to N^2
    baseline_mem_mb = (seq_len * seq_len * 2) / (1024**2) 
    
    print(f"[Baseline] Global Attention Compute: {baseline_compute}")
    print(f"[Baseline] Global Attention Memory: {baseline_mem_mb:.2f} MB")
    
    # Proposed: Adaptive Global-Local Attention
    # Local window size
    window_size = 256 # 16x16 window
    local_compute = seq_len * window_size
    
    # Global routing tokens (e.g. 1 per window)
    num_windows = seq_len // window_size
    global_compute = num_windows * num_windows
    
    proposed_compute = local_compute + global_compute
    proposed_mem_mb = (proposed_compute * 2) / (1024**2)
    
    speedup = baseline_compute / proposed_compute
    mem_reduction = 1.0 - (proposed_mem_mb / baseline_mem_mb)
    
    print(f"[Proposed] Adaptive Attention Compute: {proposed_compute}")
    print(f"[Proposed] Adaptive Attention Memory: {proposed_mem_mb:.2f} MB")
    print(f"Hardware Compute Speedup: {speedup:.2f}x")
    print(f"SRAM Memory Reduction: {mem_reduction*100:.2f}%")
    
    # Check if it fits in SRAM
    if proposed_mem_mb < sram_capacity_mb:
        print("Status: Fits entirely in Edge NPU SRAM (No DRAM Thrashing).")
    else:
        print("Status: Still requires DRAM.")

if __name__ == "__main__":
    simulate_dit_adaptive_attention()
