import time

def simulate_vq_kv():
    # Context: 32K tokens, 8 heads, 128 dim
    context_len = 32768
    head_dim = 128
    num_heads = 8
    layers = 32
    
    # Original FP16
    fp16_size_mb = (context_len * head_dim * num_heads * layers * 2 * 2) / (1024**2)
    
    # VQ parameters (e.g., 256 codebook size -> 8 bits, block size 4)
    block_size = 4
    bits_per_block = 8
    compression_ratio = (16 * block_size) / bits_per_block
    
    vq_size_mb = fp16_size_mb / compression_ratio
    
    # Hardware SRAM read latency
    sram_bw_gbps = 2000.0 # 2 TB/s Edge NPU SRAM
    fp16_latency_us = (fp16_size_mb / 1024) / sram_bw_gbps * 1000000
    vq_latency_us = (vq_size_mb / 1024) / sram_bw_gbps * 1000000
    
    # VQ lookup overhead (LUT reads)
    vq_lut_reads = (context_len * head_dim * num_heads * layers * 2) / block_size
    lut_latency_us = vq_lut_reads * 0.000001 # 1ns per concurrent block lookup
    
    total_vq_latency = vq_latency_us + lut_latency_us
    
    print("--- Vector Quantization (VQ) KV Cache Hardware Simulation ---")
    print(f"FP16 KV Cache Size: {fp16_size_mb:.2f} MB")
    print(f"VQ KV Cache Size: {vq_size_mb:.2f} MB (Ratio: {compression_ratio}x)")
    print(f"FP16 Read Latency: {fp16_latency_us:.2f} us")
    print(f"VQ (Read + LUT Decode) Latency: {total_vq_latency:.2f} us")
    print("Conclusion: VQ significantly reduces SRAM footprint but introduces LUT decoding overhead. Requires dedicated SRAM Codebook Arrays.")

if __name__ == "__main__":
    simulate_vq_kv()
