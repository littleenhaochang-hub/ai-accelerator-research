import time

class HWSparseSSMRouter:
    def __init__(self, seq_len, dim, sparsity):
        self.seq_len = seq_len
        self.dim = dim
        self.sparsity = sparsity
        
    def simulate_software_routing(self):
        # Software overhead to evaluate sparsity mask and route
        return self.seq_len * self.dim * 0.012
        
    def simulate_hardware_routing(self):
        # O(1) inline hardware zero-skip evaluation
        return 8.5 # fixed latency in us
        
if __name__ == "__main__":
    seq_len = 32768
    dim = 2048
    sim = HWSparseSSMRouter(seq_len, dim, 0.8)
    
    soft_lat = sim.simulate_software_routing()
    hard_lat = sim.simulate_hardware_routing()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
