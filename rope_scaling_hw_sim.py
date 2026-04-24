import time

def software_rope_scaling(seq_len, d_head, scale_factor):
    # Simulated latency for software dynamic RoPE scaling (e.g. YaRN, NTK-Aware)
    # Requires recomputing base frequencies and interpolating phase angles dynamically on CPU/GPU
    latency = seq_len * d_head * 0.0015 # ms
    return latency

def hardware_rope_scaler(seq_len, d_head, scale_factor):
    # Simulated latency for an inline Hardware Dynamic RoPE Scaler
    # Shifts and interpolates frequencies in hardware registers in 1 cycle
    latency = seq_len * d_head * 0.0001 # ms
    return latency

def main():
    seq_len = 128000 # Extreme long context requiring scaling
    d_head = 128
    scale_factor = 4.0 # Extending 32K context to 128K
    
    print("Running Hardware Dynamic RoPE Scaling Simulation...")
    sw_lat = software_rope_scaling(seq_len, d_head, scale_factor)
    print(f"Software RoPE Scaling Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_rope_scaler(seq_len, d_head, scale_factor)
    print(f"Hardware RoPE Scaling Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
