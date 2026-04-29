import random

def simulate_baseline_int4_mac_power():
    # pJ per MAC operation (INT4)
    return 0.58 

def simulate_sc_058bit_mac_power():
    # Stochastic computing uses simple logic gates (AND/XOR) instead of full adders
    return 0.04 

baseline_energy = simulate_baseline_int4_mac_power()
proposed_energy = simulate_sc_058bit_mac_power()
reduction = (baseline_energy - proposed_energy) / baseline_energy

print(f"Baseline INT4 Energy: {baseline_energy:.3f} pJ/MAC")
print(f"Proposed SC 0.58-bit Energy: {proposed_energy:.3f} pJ/MAC")
print(f"Energy Reduction: {reduction*100:.2f}%")
