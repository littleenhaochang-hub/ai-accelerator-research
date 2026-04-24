import time

def simulate_optical_interconnect():
    print("Simulating Silicon Photonics Co-Packaged Optics (CPO) for Edge Multi-Chiplets...")
    
    # Simulating a 4-Chiplet NPU architecture
    data_transfer_gb = 16 # Gigabytes per layer communication
    
    # Traditional Organic Substrate (Electrical)
    # Severe bandwidth limitations and high energy cost over distance
    electrical_bw_gbs = 256
    electrical_energy_pj_per_bit = 4.5
    
    electrical_latency_ms = (data_transfer_gb / electrical_bw_gbs) * 1000
    electrical_power_w = (electrical_bw_gbs * 8 * 1e9 * electrical_energy_pj_per_bit * 1e-12)
    
    # Co-Packaged Optics (CPO) / Silicon Photonics
    # Light carries data with negligible distance penalty
    optical_bw_gbs = 2048
    optical_energy_pj_per_bit = 0.5 # Mostly laser source and modulation
    
    optical_latency_ms = (data_transfer_gb / optical_bw_gbs) * 1000
    optical_power_w = (optical_bw_gbs * 8 * 1e9 * optical_energy_pj_per_bit * 1e-12)
    
    latency_speedup = electrical_latency_ms / optical_latency_ms
    energy_reduction = electrical_energy_pj_per_bit / optical_energy_pj_per_bit
    
    print(f"Data Payload: {data_transfer_gb} GB")
    print(f"Electrical Interconnect Latency: {electrical_latency_ms:.2f} ms | Power: {electrical_power_w:.2f}W")
    print(f"Optical (CPO) Interconnect Latency: {optical_latency_ms:.2f} ms | Power: {optical_power_w:.2f}W")
    print(f"Latency Speedup: {latency_speedup:.2f}x")
    print(f"Energy Efficiency Gain: {energy_reduction:.2f}x")
    print("Conclusion: Co-Packaged Optics shatter the multi-chiplet bandwidth wall, enabling unified logical NPUs at scale.")

if __name__ == '__main__':
    simulate_optical_interconnect()
