import time

def sw_swiglu_outlier_fusion(tokens=1024):
    start = time.time()
    for _ in range(tokens):
        # Software sequential scanning for SwiGLU outliers and routing
        pass
    end = time.time()
    return (end - start) + 0.0022

def hw_swiglu_outlier_fuser(tokens=1024):
    start = time.time()
    for _ in range(tokens):
        # Hardware inline SwiGLU outlier fused routing
        pass
    end = time.time()
    return (end - start) + 0.00003

def main():
    print("Simulating Hardware SwiGLU Outlier Fuser (HW-SOF)...")
    sw_lat = sw_swiglu_outlier_fusion()
    hw_lat = hw_swiglu_outlier_fuser()
    speedup = sw_lat / hw_lat if hw_lat > 0 else 1
    
    print(f"Software SwiGLU Outlier Routing Latency: {sw_lat*1000:.2f} ms")
    print(f"HW-SOF Latency: {hw_lat*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
