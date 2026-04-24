import time

def software_minmax_scaling(tensor_size):
    # Simulated CPU/GPU software latency for dynamic min-max scaling of a tensor
    # Find min, find max, compute scale/zero-point, then apply
    latency = tensor_size * 0.002 # ms
    return latency

def hardware_minmax_scaler(tensor_size):
    # Simulated latency of an inline hardware min-max accumulator and scaler
    # Computed on the fly during SRAM read/write without separate passes
    latency = tensor_size * 0.0001 # ms
    return latency

def main():
    tensor_size = 8192 # typical sequence length or channel size
    print("Running Hardware Dynamic Min-Max Scaler Simulation...")
    sw_lat = software_minmax_scaling(tensor_size)
    print(f"Software Scaling Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_minmax_scaler(tensor_size)
    print(f"Hardware Inline Scaler Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
