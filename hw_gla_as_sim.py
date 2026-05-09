import numpy as np

def simulate_hw_gla_associative_scan(seq_len, dim):
    print(f"Simulating Hardware GLA Associative Scanner (HW-GLA-AS) - Seq: {seq_len}, Dim: {dim}")
    
    # Software Scan: Sequential O(N) dependency
    # Recurrent update: S_t = S_{t-1} * decay + V_t
    # Memory bound and purely sequential in naive software
    sw_latency = (seq_len * dim) / (100e9) * 1000  # Purely sequential bottleneck, very low effective BW
    
    # HW-GLA-AS: Inline hardware tree for parallel associative scan O(log N)
    # Fused MAC operations in a balanced binary tree directly inside SRAM
    hw_latency = (np.log2(seq_len) * dim) / (4000e9) * 1000 # Parallel processing, high internal BW
    
    print(f"Software Sequential Scan Latency: {sw_latency:.4f} ms")
    print(f"HW-GLA-AS Parallel Latency: {hw_latency:.4f} ms")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_gla_associative_scan(65536, 1024)
