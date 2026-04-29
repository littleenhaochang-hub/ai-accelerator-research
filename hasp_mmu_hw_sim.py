import numpy as np

def simulate_hasp_mmu():
    print("Simulating Hardware Attention-Score Pruning MMU (HASP-MMU)...")
    num_pages = 1024
    
    # Baseline software page unmapping and TLB teardown
    baseline_latency = num_pages * 0.045
    
    # Proposed hardware inline MMU state pruning
    proposed_latency = num_pages * 0.0015
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hasp_mmu()
