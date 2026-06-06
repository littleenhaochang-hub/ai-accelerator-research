import random
import math

def simulate_mamba_state_size(seq_len, d_state, d_model):
    return seq_len * d_state * d_model * 2 # Bytes (FP16)

def simulate_hw_dsc_latency(seq_len, d_state, d_model, hardware_type="baseline"):
    base_latency = (seq_len * d_state * d_model) * 0.0000005 # Baseline SRAM/DRAM traffic delay
    if hardware_type == "baseline":
        return base_latency
    elif hardware_type == "hw_dsc":
        # Dynamic State Compressor uses low-rank projection in hardware, 
        # cutting traffic significantly at the cost of a small inline projection MAC delay
        return (base_latency * 0.15) + (seq_len * d_model * 0.000001)

if __name__ == "__main__":
    seq_len = 128000
    d_state = 16
    d_model = 4096
    
    baseline_size_mb = simulate_mamba_state_size(seq_len, d_state, d_model) / (1024*1024)
    dsc_size_mb = baseline_size_mb * 0.125 # 8x compression ratio via low-rank
    
    base_lat = simulate_hw_dsc_latency(seq_len, d_state, d_model, "baseline")
    dsc_lat = simulate_hw_dsc_latency(seq_len, d_state, d_model, "hw_dsc")
    
    speedup = base_lat / dsc_lat
    
    print(f"Baseline State Size: {baseline_size_mb:.2f} MB")
    print(f"HW-DSC State Size: {dsc_size_mb:.2f} MB")
    print(f"Baseline Memory Latency: {base_lat:.2f} ms")
    print(f"HW-DSC Latency: {dsc_lat:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
