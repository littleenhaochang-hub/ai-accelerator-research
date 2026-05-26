import time

def simulate_hw_dmta(experts=256, tokens_per_expert=128):
    # Baseline: Software gathering tokens from multiple chiplets across NoC
    software_latency_ms = experts * tokens_per_expert * 0.005 # Memory copies & NoC software overhead
    
    # Proposed: Hardware Distributed MoE Token Aggregator (HW-DMTA)
    # Direct P2P NoC hardware aggregation bypassing CPU/SRAM bounce buffers
    hardware_latency_ms = experts * tokens_per_expert * 0.0001
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Experts: {experts}, Tokens/Expert: {tokens_per_expert}")
    print(f"Baseline Latency (Software NoC): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-DMTA): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_dmta()
