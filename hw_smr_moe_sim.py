import time

def simulate_hw_smr(experts=1024):
    # Baseline: FP16 Dense MoE Router (Softmax + Top-K)
    software_latency_ms = experts * 0.015 
    
    # Proposed: Hardware Spiking MoE Router (HW-SMR)
    # Replaces FP16 MACs with event-driven 1-bit accumulators
    hardware_latency_ms = experts * 0.0002
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Experts: {experts}")
    print(f"Baseline Latency (Dense Softmax): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SMR): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_smr()
