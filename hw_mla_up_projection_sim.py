import time

def simulate_software_mla_up_projection(seq_len=8192, latent_dim=512, full_dim=4096):
    # Software: Read latent vector from SRAM, send to Tensor Core, compute up-projection, write back full vectors
    print(f"Simulating Software MLA Up-Projection...")
    latency = seq_len * (latent_dim * full_dim) * 0.00000005 # Software MAC overhead
    return latency

def simulate_hardware_mla_up_projection_engine(seq_len=8192, latent_dim=512, full_dim=4096):
    # HW-MLA-UPE: Dedicated hardware multiplier array directly at the SRAM read port
    print(f"Simulating Hardware MLA Up-Projection Engine (HW-MLA-UPE)...")
    latency = seq_len * (latent_dim * full_dim) * 0.000000001 # Hardware inline overhead
    return latency

if __name__ == "__main__":
    sw_lat = simulate_software_mla_up_projection()
    hw_lat = simulate_hardware_mla_up_projection_engine()
    
    print(f"Software Up-Projection Latency: {sw_lat:.5f} s")
    print(f"HW-MLA-UPE Latency: {hw_lat:.5f} s")
    print(f"Latency Speedup: {sw_lat/hw_lat:.2f}x")
