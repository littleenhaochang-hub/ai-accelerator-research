import numpy as np

def simulate_mla_hardware(seq_len=2048, latent_dim=512, full_dim=4096, num_heads=32):
    print("=== DeepSeek MLA (Multi-Head Latent Attention) Hardware Simulation ===")
    
    # Baseline: MHA (Multi-Head Attention)
    # KV cache stores full_dim for K and V
    baseline_kv_cache_size = seq_len * full_dim * 2 * 2 # 2 for K/V, 2 bytes for FP16
    
    # Proposed: MLA Latent Cache
    # KV cache stores only the latent vector. Up-projection happens on-the-fly in SRAM.
    # We store latent_dim per token
    mla_kv_cache_size = seq_len * latent_dim * 2 # 1 latent vector, 2 bytes for FP16
    
    # But MLA requires up-projection weights
    up_proj_weights = latent_dim * full_dim * 2 * 2 # weights for K, V
    
    # Calculate Memory Bandwidth required to read KV cache for a single decoding step
    # Baseline reads the full KV cache
    baseline_read_bytes = baseline_kv_cache_size
    
    # MLA reads the latent cache + up-proj weights (if weights are not pinned in SRAM)
    # Assuming weights are pinned in SRAM or L2 cache for the NPU
    mla_read_bytes = mla_kv_cache_size 
    
    bandwidth_reduction = 1.0 - (mla_read_bytes / baseline_read_bytes)
    
    print(f"[Baseline] MHA KV Cache Read Bandwidth per Step: {baseline_read_bytes / 1024:.2f} KB")
    print(f"[Proposed] MLA Latent Cache Read Bandwidth per Step: {mla_read_bytes / 1024:.2f} KB")
    print(f"Memory Bandwidth Reduction: {bandwidth_reduction*100:.2f}%")
    print("Requirement: Hardware must support On-the-fly Up-projection from Latent Cache in the SRAM Matrix Engine.")

if __name__ == "__main__":
    simulate_mla_hardware()
