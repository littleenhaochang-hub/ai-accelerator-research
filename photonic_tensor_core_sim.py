import time

def simulate_photonic_tensor_core():
    print("Simulating Photonic Tensor Core (PTC) for LLM Linear Projections...")
    
    # 8Kx8K matrix multiplication
    N = 8192
    mac_operations = N * N * N # for N x N * N x N, actually vector-matrix is N^2.
    # Let's assume vector-matrix multiplication for decoding: 1 x N * N x N = N^2 MACs
    macs_per_token = N * N
    
    # Digital Tensor Core (INT4)
    digital_energy_per_mac_pj = 0.5 # picoJoules
    digital_latency_ns = 15.0
    
    digital_energy_total_nj = (macs_per_token * digital_energy_per_mac_pj) / 1000
    
    # Photonic Tensor Core (Analog Optical)
    # Energy is dominated by Laser DAC/ADC conversion, not the actual optical MAC
    dac_adc_energy_per_element_pj = 2.0
    photonic_energy_total_nj = (N * dac_adc_energy_per_element_pj * 2) / 1000 # Read input vector + write output vector
    
    photonic_latency_ns = 2.5 # Speed of light through Mach-Zehnder Interferometer meshes
    
    energy_reduction_factor = digital_energy_total_nj / photonic_energy_total_nj
    speedup = digital_latency_ns / photonic_latency_ns
    
    print(f"Vector-Matrix MACs: {macs_per_token:,}")
    print(f"Digital NPU Energy: {digital_energy_total_nj:.2f} nJ")
    print(f"Photonic NPU Energy: {photonic_energy_total_nj:.2f} nJ")
    print(f"Energy Reduction: {energy_reduction_factor:.2f}x")
    print(f"Latency Speedup: {speedup:.2f}x")
    print("Conclusion: Photonic crossbars provide massive energy savings for dense linear projections, bounded only by DAC/ADC overhead.")

if __name__ == '__main__':
    simulate_photonic_tensor_core()
