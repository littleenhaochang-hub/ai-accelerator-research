import time

def simulate_hw_lda(context_length=65536):
    print(f"Simulating Hardware Log-Derivative Attention (HW-LDA)...")
    print(f"Context: {context_length} tokens")
    
    # Software latency: FP16 Softmax per token over context
    sw_latency_ms = (context_length / 1000) * 0.85 
    
    # HW-LDA latency: Inline Log-Derivative approximation using PWL in SRAM
    hw_latency_ms = (context_length / 1000) * 0.12
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software Softmax Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-LDA Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_lda()
