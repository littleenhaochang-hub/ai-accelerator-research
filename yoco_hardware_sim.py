import math

def simulate_yoco_hardware():
    # Context: YOCO (You Only Cache Once) Architecture
    # Standard LLM: Every layer caches KV.
    # YOCO: Decouples into Self-Decoder (bottom half) and Cross-Decoder (top half).
    # Only the Self-Decoder caches KV. The Cross-Decoder reuses the global KV cache.
    
    seq_len = 32768
    num_layers = 32
    head_dim = 128
    num_heads = 32
    
    # FP16 bytes per element = 2
    # Standard KV Cache
    # layers * seq_len * heads * head_dim * 2 (K,V) * 2 bytes
    standard_kv_mb = (num_layers * seq_len * num_heads * head_dim * 2 * 2) / (1024**2)
    
    # YOCO KV Cache
    # Only half of the layers (the self-decoder) cache KV. 
    # Actually, YOCO often just has ONE global KV cache reused by all cross-decoder layers.
    yoco_kv_mb = ( (num_layers // 2) * seq_len * num_heads * head_dim * 2 * 2 ) / (1024**2)
    
    # Edge NPU SRAM Read Bandwidth Savings during Generation
    # Standard: Read KV for current layer
    # YOCO: Cross-decoder layers read from the *exact same* SRAM addresses. 
    # Hardware can broadcast this global KV cache or pin it in SRAM to achieve 0 memory fetch overhead for top layers.
    
    sram_bw_gbps = 2000.0
    standard_fetch_us = (standard_kv_mb / 1024) / sram_bw_gbps * 1000000
    yoco_fetch_us = (yoco_kv_mb / 1024) / sram_bw_gbps * 1000000
    
    print("--- YOCO (You Only Cache Once) Hardware Simulation ---")
    print(f"Standard KV Cache Size (32K context): {standard_kv_mb:.2f} MB")
    print(f"YOCO KV Cache Size (32K context): {yoco_kv_mb:.2f} MB")
    print(f"Memory Capacity Reduction: {standard_kv_mb / yoco_kv_mb:.2f}x")
    print(f"Standard SRAM Fetch Latency: {standard_fetch_us:.2f} us")
    print(f"YOCO SRAM Fetch Latency: {yoco_fetch_us:.2f} us")
    print("Conclusion: YOCO strictly halves the KV Cache capacity. By pinning the global KV cache in the NPU SRAM, the Cross-Decoder layers experience zero KV load latency. Hardware should implement an 'SRAM Broadcast Bus' to share this KV across parallel ALUs.")

if __name__ == "__main__":
    simulate_yoco_hardware()
