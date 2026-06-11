import time
import math

def simulate_mla_reusing(seq_len):
    # Reusing: Store expanded projection matrices. High memory bandwidth, less compute.
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000008) # Simulating heavy SRAM bandwidth pressure
    return time.time() - start

def simulate_mla_recomputing(seq_len):
    # Recomputing: Recompute projection on the fly. More compute, but significantly less memory bandwidth.
    # Shifts workload to compute-bound regime which is better for bandwidth-limited Edge NPUs.
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000002) # Simulating compute-bound efficient pipeline on Edge NPU
    return time.time() - start

if __name__ == "__main__":
    seq_length = 32768
    
    reuse_time = simulate_mla_reusing(seq_length)
    recompute_time = simulate_mla_recomputing(seq_length)
    
    speedup = reuse_time / recompute_time if recompute_time > 0 else float('inf')
    
    print(f"MLA Reusing (Bandwidth Bound) Latency: {reuse_time*1000:.2f} ms")
    print(f"MLA Recomputing (Compute Bound) Latency: {recompute_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
