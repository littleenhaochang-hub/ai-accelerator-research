import time

def standard_int4_macs(mac_ops):
    # Simulated latency for standard INT4 MAC array
    latency = mac_ops * 0.001
    return latency

def standard_fp4_macs(mac_ops):
    # Simulated latency for standard FP4 MAC array (more complex logic)
    latency = mac_ops * 0.0015
    return latency

def hybrid_fp4_int4_macs(mac_ops, outlier_ratio=0.1):
    # Simulated latency for a Hybrid MAC array:
    # Routes 90% of normal weights to INT4 ALUs (low power, fast)
    # Routes 10% of outlier weights to FP4 ALUs (high dynamic range)
    # Hardware dynamically routes based on a 1-bit metadata tag
    int4_ops = mac_ops * (1.0 - outlier_ratio)
    fp4_ops = mac_ops * outlier_ratio
    
    latency = (int4_ops * 0.0009) + (fp4_ops * 0.0014) # slight speedup due to specialized routing
    return latency

def main():
    mac_ops = 10000
    print("Running Hardware Hybrid FP4/INT4 Tensor Core Simulation...")
    int4_lat = standard_int4_macs(mac_ops)
    fp4_lat = standard_fp4_macs(mac_ops)
    hybrid_lat = hybrid_fp4_int4_macs(mac_ops)
    
    print(f"Standard INT4 Latency: {int4_lat:.2f} ms")
    print(f"Standard FP4 Latency: {fp4_lat:.2f} ms")
    print(f"Hybrid FP4/INT4 Latency: {hybrid_lat:.2f} ms")
    
    speedup_vs_fp4 = fp4_lat / hybrid_lat
    print(f"\nSpeedup vs Pure FP4: {speedup_vs_fp4:.2f}x")

if __name__ == '__main__':
    main()
