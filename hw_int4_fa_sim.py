import time

def simulate_hw_int4_fa(context_length=32768, head_dim=128):
    print(f"Simulating Hardware INT4 FlashAttention Engine (HW-INT4-FA)...")
    print(f"Context: {context_length} tokens, Head Dim: {head_dim}")
    
    # FP16 FlashAttention SRAM bandwidth overhead
    fp16_bytes = context_length * head_dim * 2 # 2 bytes per element
    sw_latency_ms = (fp16_bytes / (1024**2)) * 0.45 
    
    # INT4 FlashAttention SRAM bandwidth overhead (0.5 bytes per element) + inline dequant
    int4_bytes = context_length * head_dim * 0.5
    hw_latency_ms = (int4_bytes / (1024**2)) * 0.45 + 0.1 # Small inline dequant penalty
    
    speedup = sw_latency_ms / hw_latency_ms
    bandwidth_reduction = fp16_bytes / int4_bytes
    
    print(f"FP16 FA Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-INT4-FA Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SRAM Bandwidth Reduction: {bandwidth_reduction:.2f}x")

if __name__ == "__main__":
    simulate_hw_int4_fa()
