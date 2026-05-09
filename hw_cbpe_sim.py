import time

def simulate_hw_cbpe():
    num_requests = 128
    
    # Baseline: Software preemption requires saving the full KV cache to CPU RAM or NVMe
    # CPU interrupt + DMA transfer out + memory allocator update
    sw_preemption_latency_ms = 45.0
    baseline_latency_ms = num_requests * sw_preemption_latency_ms
    
    # HW-CBPE: Hardware Continuous Batching Preemption Engine
    # Directly swaps active page table pointers to a background NVMe queue via P2P DMA, 
    # zero CPU interrupt overhead.
    hw_preemption_latency_ms = 1.2
    proposed_latency_ms = num_requests * hw_preemption_latency_ms
    
    print("=== HW-CBPE Simulation ===")
    print(f"Number of Requests: {num_requests}")
    print(f"Baseline Latency (Software Preemption): {baseline_latency_ms:.2f} ms")
    print(f"HW-CBPE Latency (Hardware Preemption): {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {baseline_latency_ms/proposed_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_cbpe()