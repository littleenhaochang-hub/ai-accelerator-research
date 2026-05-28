import time

class HWSLASimulator:
    def __init__(self, seq_len=65536, dim=1024):
        self.seq_len = seq_len
        self.dim = dim
        self.dense_mac_energy_pj = 0.5
        self.spike_add_energy_pj = 0.05
        
    def simulate_dense(self):
        # Dense Linear Attention State Update
        macs = self.seq_len * self.dim * self.dim
        energy = macs * self.dense_mac_energy_pj
        latency = macs / (100e9) * 1000 # ms
        return latency, energy
        
    def simulate_hw_sla(self, spike_rate=0.15):
        # Spiking Linear Attention: Only active spikes trigger an Add operation (Zero MACs)
        active_adds = self.seq_len * self.dim * self.dim * spike_rate
        energy = active_adds * self.spike_add_energy_pj
        
        # Asynchronous event-driven updates avoid dense matrix bottlenecks
        latency = active_adds / (100e9) * 1000 # ms
        return latency, energy

if __name__ == "__main__":
    print("Simulating Hardware Spiking Linear Attention (HW-SLA)...")
    sim = HWSLASimulator()
    
    base_lat, base_energy = sim.simulate_dense()
    hw_lat, hw_energy = sim.simulate_hw_sla(spike_rate=0.12)
    
    print(f"Baseline - Latency: {base_lat:.2f} ms, Energy: {base_energy:.2f} pJ")
    print(f"HW-SLA - Latency: {hw_lat:.2f} ms, Energy: {hw_energy:.2f} pJ")
    print(f"Latency Speedup: {base_lat/hw_lat:.2f}x")
    print(f"Energy Reduction: {(base_energy-hw_energy)/base_energy*100:.2f}%")
