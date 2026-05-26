import time

class HWKVTemporalCompressor:
    def __init__(self, seq_len, dim):
        self.seq_len = seq_len
        self.dim = dim
        
    def simulate_software_delta(self):
        # O(N) software delta encoding latency
        return self.seq_len * self.dim * 0.008
        
    def simulate_hardware_delta(self):
        # O(1) hardware delta compression at SRAM write port
        return 12.5 # fixed latency in us
        
if __name__ == "__main__":
    seq_len = 65536
    dim = 1024
    sim = HWKVTemporalCompressor(seq_len, dim)
    
    soft_lat = sim.simulate_software_delta()
    hard_lat = sim.simulate_hardware_delta()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
