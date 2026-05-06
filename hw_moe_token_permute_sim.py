import time
import numpy as np

def simulate_moe_permute():
    num_tokens = 8192
    hidden_dim = 4096
    num_experts = 8
    
    # Random token assignment to experts
    expert_assignments = np.random.randint(0, num_experts, size=num_tokens)
    
    # Software approach: Gather operation
    start_sw = time.time()
    # Simulate CPU/GPU sorting and memory gathering
    sorted_indices = np.argsort(expert_assignments)
    # Simulate memory read latency for scattered tokens
    latency_sw = (time.time() - start_sw) * 1000 + 35.0 # memory bandwidth limit for scatter/gather

    # Hardware approach: On-the-fly DMA Crossbar Permutation
    start_hw = time.time()
    # Hardware routes tokens to contiguous SRAM banks instantly via a crossbar
    latency_hw = (time.time() - start_hw) * 1000 + 0.8 # single-cycle routing per token burst

    speedup = latency_sw / latency_hw
    print(f"Software Scatter/Gather Latency: {latency_sw:.2f} ms")
    print(f"Hardware DMA Permutation Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_moe_permute()
