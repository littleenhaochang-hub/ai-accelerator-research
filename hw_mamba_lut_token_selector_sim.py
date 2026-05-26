import time
import math

class HWMambaLUTTokenSelector:
    def __init__(self, seq_len, dim):
        self.seq_len = seq_len
        self.dim = dim
        
    def simulate_software_selection(self):
        # O(N) software token selection
        latency_us = self.seq_len * self.dim * 0.005
        return latency_us
        
    def simulate_hardware_lut_selection(self):
        # O(1) LUT-based parallel selection
        latency_us = 10.0 # Fixed hardware lookup latency
        return latency_us

if __name__ == "__main__":
    seq_len = 32768
    dim = 2048
    sim = HWMambaLUTTokenSelector(seq_len, dim)
    
    soft_lat = sim.simulate_software_selection()
    hard_lat = sim.simulate_hardware_lut_selection()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware LUT Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
