import numpy as np

def simulate_cim_sram_energy(dim=4096):
    print("=== SRAM Compute-in-Memory (CIM) Energy Simulation ===")
    
    # Baseline: Digital NPU Tensor Core (4-bit)
    # Energy to read 4-bit weight from SRAM: ~2.0 pJ
    # Energy to read 4-bit activation: ~2.0 pJ
    # Energy for digital 4-bit MAC: ~0.1 pJ
    # Energy to write to accumulator: ~0.5 pJ
    baseline_energy_per_mac_pj = 4.6
    
    # Proposed: Analog/Digital SRAM CIM (4-bit)
    # Weights stay in SRAM cells. Activations drive wordlines.
    # Bitlines accumulate current (analog MAC). ADC converts back to digital.
    # Energy per CIM MAC (amortizing ADC over 256 rows): ~0.4 pJ
    cim_energy_per_mac_pj = 0.4
    
    num_macs = dim * dim
    
    baseline_total_pj = num_macs * baseline_energy_per_mac_pj
    proposed_total_pj = num_macs * cim_energy_per_mac_pj
    
    energy_savings = 1.0 - (proposed_total_pj / baseline_total_pj)
    
    print(f"[Baseline] Digital Tensor Core Energy: {baseline_total_pj / 1e6:.2f} uJ")
    print(f"[Proposed] SRAM CIM Energy: {proposed_total_pj / 1e6:.2f} uJ")
    print(f"Hardware Energy Reduction: {energy_savings*100:.2f}%")

if __name__ == "__main__":
    simulate_cim_sram_energy()
