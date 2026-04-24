import time

def systolic_array_gemv(tokens, d_model):
    # Simulated latency for GEMV (batch=1 decoding) on a dense Systolic Array
    # Systolic arrays suffer from extremely poor utilization (e.g., <5%) during matrix-vector multiplication
    latency = tokens * d_model * 0.002 # ms
    return latency

def vector_mac_engine_gemv(tokens, d_model):
    # Simulated latency for a dedicated Vector-MAC (VMAC) Engine tailored for Decode
    # 100% utilization, directly attached to high-bandwidth SRAM banks
    latency = tokens * d_model * 0.0001 # ms
    return latency

def main():
    tokens = 2048 # Decoding tokens one by one (batch=1)
    d_model = 4096
    
    print("Running Hardware GEMV Decode Engine Simulation...")
    sys_lat = systolic_array_gemv(tokens, d_model)
    print(f"Systolic Array Decode Latency: {sys_lat:.2f} ms")
    
    vmac_lat = vector_mac_engine_gemv(tokens, d_model)
    print(f"Dedicated VMAC Decode Latency: {vmac_lat:.2f} ms")
    
    speedup = sys_lat / vmac_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
