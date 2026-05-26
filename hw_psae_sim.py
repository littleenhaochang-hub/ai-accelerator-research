import time

def simulate_hw_psae(batch_size=128, prefix_tokens=4096, d_model=4096):
    # Baseline: Software prefix caching for Continuous Batching
    # Even with shared memory pointers, the SRAM must read the prefix 128 times to feed different batch MACs
    software_latency_ms = batch_size * (prefix_tokens * d_model * 2 / (1024**2)) * 0.5 
    
    # Proposed: Hardware Prefix-Shared Attention Engine (HW-PSAE)
    # Reads the prefix from SRAM ONCE and multicasts it over a hardware bus to all 128 MAC arrays simultaneously
    hardware_latency_ms = (prefix_tokens * d_model * 2 / (1024**2)) * 0.5 + 0.01 # single read + multicast overhead
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Batch Size: {batch_size}, Shared Prefix Tokens: {prefix_tokens}")
    print(f"Baseline Latency (Repeated SRAM Reads): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-PSAE Multicast): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_psae()
