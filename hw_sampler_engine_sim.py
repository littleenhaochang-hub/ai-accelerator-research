import time

def simulate_hw_sampler(vocab_size):
    print(f"Simulating Hardware Top-K/Top-P Sampler Engine for vocab size {vocab_size}...")
    # Software: PCIe transfer of logits + CPU sort/softmax/sample
    sw_latency = vocab_size * 0.00005 + 0.5 
    
    # Hardware: On-chip parallel sort, softmax, and PRNG sampling
    hw_latency = vocab_size * 0.000001 
    
    speedup = sw_latency / hw_latency
    
    print(f"SW Latency (CPU + PCIe): {sw_latency:.4f} ms")
    print(f"HW Latency (On-Chip): {hw_latency:.4f} ms")
    print(f"Speedup: {speedup:.2f}x")
    return speedup

simulate_hw_sampler(128256)
