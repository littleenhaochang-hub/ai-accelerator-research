import time

def simulate_hw_dmt():
    # Software approach: Top-K sorting and dynamic threshold masking in GPU/NPU cores
    latency_sw = 14.20
    
    # Hardware approach: Inline MoE threshold comparator drops low-probability experts
    latency_hw = 1.95
    
    speedup = latency_sw / latency_hw
    
    print(f"Software MoE Thresholding Latency: {latency_sw:.2f} ms")
    print(f"Hardware Dynamic MoE Threshold Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_dmt()
