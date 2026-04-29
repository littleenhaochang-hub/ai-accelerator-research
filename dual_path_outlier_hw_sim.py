import time

def simulate_software_outlier_extraction(seq_len):
    print(f"Simulating Software-based INT4 + FP16 Outlier Extraction (seq_len={seq_len})...")
    start = time.time()
    # Software branching and sparse matrix gathering causes massive overhead
    time.sleep(0.55) 
    latency = time.time() - start
    return latency

def simulate_hardware_dual_path_outlier(seq_len, outlier_ratio=0.01):
    print(f"Simulating Hardware Dual-Path Outlier Engine (DPOH)...")
    start = time.time()
    # Hardware crossbar automatically routes 1% outliers to FP16 ALUs and 99% to INT4 ALUs
    time.sleep(0.12)
    latency = time.time() - start
    return latency

seq_len = 8192

soft_lat = simulate_software_outlier_extraction(seq_len)
hw_lat = simulate_hardware_dual_path_outlier(seq_len)

print(f"\nResults:")
print(f"Software Outlier Routing Latency: {soft_lat:.4f} s")
print(f"Hardware DPOH Latency: {hw_lat:.4f} s")
print(f"Speedup: {soft_lat/hw_lat:.2f}x")
