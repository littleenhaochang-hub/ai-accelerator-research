import time

def simulate_rram_cim():
    print("Simulating RRAM Compute-in-Memory (CIM) vs SRAM for LLM Weights...")
    
    # 7B model at INT4 -> 3.5GB weights
    model_size_mb = 3500
    
    # SRAM Baseline
    sram_leakage_power_mw_per_mb = 2.5
    sram_total_leakage_mw = model_size_mb * sram_leakage_power_mw_per_mb
    
    sram_read_energy_pj_per_bit = 0.5
    
    # RRAM (Resistive RAM) CIM
    rram_leakage_power_mw_per_mb = 0.01 # Non-volatile, near zero leakage
    rram_total_leakage_mw = model_size_mb * rram_leakage_power_mw_per_mb
    
    rram_cim_energy_pj_per_bit = 0.1 # Compute directly on the crossbar
    
    leakage_reduction = sram_total_leakage_mw / rram_total_leakage_mw
    energy_reduction = sram_read_energy_pj_per_bit / rram_cim_energy_pj_per_bit
    
    print(f"SRAM Static Leakage Power: {sram_total_leakage_mw:.2f} mW")
    print(f"RRAM Static Leakage Power: {rram_total_leakage_mw:.2f} mW")
    print(f"Static Power Reduction: {leakage_reduction:.2f}x")
    print(f"Dynamic Energy Reduction: {energy_reduction:.2f}x")
    print("Conclusion: RRAM CIM provides massive static power savings and dynamic efficiency for edge models.")

if __name__ == '__main__':
    simulate_rram_cim()
