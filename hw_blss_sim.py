import time
import random

class HWBLSSSimulator:
    def __init__(self, num_macs=1024*1024, bit_width=8):
        self.num_macs = num_macs
        self.bit_width = bit_width
        self.dense_energy_pj_per_mac = 0.5 # pJ
        self.cycle_time_ns = 1.0 # 1 GHz
        
    def simulate_dense_baseline(self):
        # Dense MAC computes all bits regardless of zero values
        energy = self.num_macs * self.dense_energy_pj_per_mac
        latency = self.num_macs / (1024) * self.cycle_time_ns # simplified pipelined latency
        return latency, energy
        
    def simulate_hw_blss(self, sparsity_factor=0.6):
        # HW-BLSS detects leading zeros in INT8/INT4 and clock-gates the multiplier
        # For an 8-bit integer, if top 4 bits are 0, it early-terminates the bit-serial addition
        active_macs_equivalent = self.num_macs * (1 - sparsity_factor * 0.75) # 75% power save on sparse
        energy = active_macs_equivalent * self.dense_energy_pj_per_mac
        
        # Latency improves due to early termination in an asynchronous array
        latency = (self.num_macs / 1024) * self.cycle_time_ns * (1 - sparsity_factor * 0.5) 
        return latency, energy

if __name__ == "__main__":
    print("Simulating Hardware Bit-Level Sparsity Scanner (HW-BLSS)...")
    sim = HWBLSSSimulator(num_macs=10*1024*1024, bit_width=8)
    
    base_lat, base_energy = sim.simulate_dense_baseline()
    hw_lat, hw_energy = sim.simulate_hw_blss(sparsity_factor=0.85) # High bit-level sparsity in LLMs
    
    print(f"Baseline - Latency: {base_lat:.2f} ns, Energy: {base_energy:.2f} pJ")
    print(f"HW-BLSS - Latency: {hw_lat:.2f} ns, Energy: {hw_energy:.2f} pJ")
    print(f"Latency Speedup: {base_lat/hw_lat:.2f}x")
    print(f"Energy Reduction: {(base_energy-hw_energy)/base_energy*100:.2f}%")
