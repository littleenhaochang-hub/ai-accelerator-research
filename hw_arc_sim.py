import time

class HWActivationRangeCollector:
    def __init__(self, seq_len, dim):
        self.seq_len = seq_len
        self.dim = dim
        
    def simulate_software_collection(self):
        # Software overhead to find min/max for dynamic quantization
        return self.seq_len * self.dim * 0.015
        
    def simulate_hardware_collection(self):
        # O(1) inline hardware min/max tracker at SRAM write port
        return 12.0 # fixed latency in us
        
if __name__ == "__main__":
    seq_len = 16384
    dim = 2048
    sim = HWActivationRangeCollector(seq_len, dim)
    
    soft_lat = sim.simulate_software_collection()
    hard_lat = sim.simulate_hardware_collection()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
