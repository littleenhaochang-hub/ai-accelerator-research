import time

def simulate_hw_bska():
    seq_len = 32768
    head_dim = 128
    
    # Baseline: INT8 MAC array computes full 8-bit dot products for all tokens
    # Power and latency are proportional to bit-width * sequence length
    baseline_latency_ms = 4.5 # ms per attention chunk
    baseline_energy_uj = 1500.0 # microjoules
    
    # HW-BSKA: Bit-Serial MAC arrays.
    # Computes MSB (Most Significant Bit) first. 
    # Hardware aborts 75% of dot products after the top 3 bits if the partial sum is too low.
    # The remaining 25% (important tokens) need the full 8 bits.
    avg_bits_computed = (0.75 * 3) + (0.25 * 8)
    
    # Speedup and energy reduction are proportional to bit reduction (ideal case)
    bit_reduction_ratio = avg_bits_computed / 8.0
    
    # Add 10% hardware overhead for bit-serial routing and abort logic
    proposed_latency_ms = baseline_latency_ms * bit_reduction_ratio * 1.1 
    proposed_energy_uj = baseline_energy_uj * bit_reduction_ratio
    
    print("=== HW-BSKA Simulation ===")
    print(f"Context Length: {seq_len}, Head Dim: {head_dim}")
    print(f"Baseline Latency (INT8 Dense MAC): {baseline_latency_ms:.2f} ms")
    print(f"HW-BSKA Latency (Bit-Serial Abort): {proposed_latency_ms:.2f} ms")
    print(f"Baseline Energy: {baseline_energy_uj:.2f} uJ")
    print(f"HW-BSKA Energy: {proposed_energy_uj:.2f} uJ")
    print(f"Speedup: {baseline_latency_ms/proposed_latency_ms:.2f}x")
    print(f"Energy Reduction: {(1 - proposed_energy_uj/baseline_energy_uj)*100:.2f}%")

if __name__ == '__main__':
    simulate_hw_bska()