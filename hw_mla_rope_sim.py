import time

def simulate_hw_mla_rope():
    seq_len = 8192
    dim = 4096
    
    # Baseline: Separate Up-Projection and RoPE (Software Kernel)
    # 1. Read Latent, Up-Project -> Write Uncompressed K to SRAM
    # 2. Read Uncompressed K -> Apply RoPE -> Attention
    sram_bandwidth_gbs = 2000 # 2000 GB/s
    
    # Bytes
    latent_bytes = seq_len * 512 * 2 # 512 dim latent, FP16
    uncompressed_bytes = seq_len * dim * 2 # 4096 dim uncompressed, FP16
    
    latent_read_ms = (latent_bytes / (sram_bandwidth_gbs * 1e9)) * 1000
    uncompressed_write_ms = (uncompressed_bytes / (sram_bandwidth_gbs * 1e9)) * 1000
    uncompressed_read_ms = (uncompressed_bytes / (sram_bandwidth_gbs * 1e9)) * 1000
    rope_compute_ms = 0.5 # assumed compute latency
    
    baseline_latency = latent_read_ms + uncompressed_write_ms + uncompressed_read_ms + rope_compute_ms
    
    # HW-MLA-RoPE: Inline CORDIC RoPE immediately after Up-Projection
    # No intermediate SRAM write/read for uncompressed K
    hw_rope_latency = latent_read_ms + rope_compute_ms
    
    print("=== HW-MLA-RoPE Simulation ===")
    print(f"Baseline Latency: {baseline_latency:.4f} ms")
    print(f"HW-MLA-RoPE Latency: {hw_rope_latency:.4f} ms")
    print(f"Speedup: {baseline_latency/hw_rope_latency:.2f}x")
    sram_saved = (uncompressed_write_ms + uncompressed_read_ms)
    print(f"SRAM R/W Latency Saved: {sram_saved:.4f} ms")

if __name__ == '__main__':
    simulate_hw_mla_rope()
