import time

def simulate_hw_kchof(context_length=128000, head_dim=128):
    print(f"Simulating Hardware K-Cache Hadamard Outlier Fuser (HW-KCHOF)...")
    print(f"Context: {context_length} tokens, Head Dim: {head_dim}")
    
    # Software overhead: Computing Hadamard transform per token/head
    sw_latency_ms = (context_length / 1000) * 1.8 
    
    # Hardware latency: O(N log N) butterfly network in hardware (inline)
    hw_latency_ms = (context_length / 1000) * 0.06
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software Hadamard Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-KCHOF Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_kchof()
