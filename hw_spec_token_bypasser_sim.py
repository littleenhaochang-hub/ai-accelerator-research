import time

class HWSpeculativeTokenBypasser:
    def __init__(self, seq_len, dim):
        self.seq_len = seq_len
        self.dim = dim
        
    def simulate_software_bypassing(self):
        # Software branching and memory scatter/gather overhead
        return self.seq_len * self.dim * 0.007
        
    def simulate_hardware_bypassing(self):
        # Inline hardware comparator at SRAM
        return 9.2 # fixed latency in us
        
if __name__ == "__main__":
    seq_len = 8192
    dim = 2048
    sim = HWSpeculativeTokenBypasser(seq_len, dim)
    
    soft_lat = sim.simulate_software_bypassing()
    hard_lat = sim.simulate_hardware_bypassing()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
