import time

class HWSparseVectorCompressor:
    def __init__(self, seq_len, dim, sparsity):
        self.seq_len = seq_len
        self.dim = dim
        self.sparsity = sparsity
        
    def simulate_software_compression(self):
        # Software zero-skipping and CSR/COO formatting
        return self.seq_len * self.dim * 0.018
        
    def simulate_hardware_compression(self):
        # Inline hardware bitmask generation and dense packing
        return 18.5 # fixed latency in us
        
if __name__ == "__main__":
    seq_len = 32768
    dim = 4096
    sparsity = 0.85
    sim = HWSparseVectorCompressor(seq_len, dim, sparsity)
    
    soft_lat = sim.simulate_software_compression()
    hard_lat = sim.simulate_hardware_compression()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
