import time

def simulate_hw_kv_oabp(context_length=65536, outlier_ratio=0.01):
    # Baseline: Software-based Outlier Extraction and Sparse formatting (e.g., CSR/COO)
    software_latency_ms = context_length * outlier_ratio * 0.05 # Scatter/Gather overhead
    
    # Proposed: Hardware KV Outlier-Aware Bit-Packer (HW-KV-OABP) inline at SRAM write
    hardware_latency_ms = context_length * outlier_ratio * 0.001
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Context Length: {context_length}, Outlier Ratio: {outlier_ratio}")
    print(f"Baseline Latency (Software Sparse): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-KV-OABP): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_kv_oabp()
