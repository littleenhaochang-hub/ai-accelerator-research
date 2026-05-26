import time

def simulate_hw_bfp8_kvc(context_length=128000):
    print(f"Simulating Hardware Block-wise FP8 Quantization (HW-BFP8-KVC)...")
    
    # Software overhead: Scaling and quantizing per block
    sw_latency_ms = (context_length / 1000) * 0.95 
    
    # Hardware latency: Inline exponent alignment and mantissa rounding
    hw_latency_ms = (context_length / 1000) * 0.08
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software FP8 Quantization Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-BFP8-KVC Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_bfp8_kvc()
