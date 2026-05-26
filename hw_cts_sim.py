import time

def simulate_hw_cts(context_length=256000, sparsity=0.85):
    print(f"Simulating Hardware Continuous Token Sparsity (HW-CTS)...")
    print(f"Context: {context_length} tokens, Sparsity Target: {sparsity}")
    
    # Software overhead: Re-evaluating sparsity masks over sliding window
    sw_latency_ms = (context_length / 1000) * 1.5 
    
    # Hardware latency: Continuous hardware-level token pruning
    hw_latency_ms = (context_length / 1000) * 0.05
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software CTS Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-CTS Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_cts()
