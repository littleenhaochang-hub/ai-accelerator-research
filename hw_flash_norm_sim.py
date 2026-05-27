import time

class HW_FlashNorm:
    def __init__(self, seq_len=32768, dim=4096):
        self.seq_len = seq_len
        self.dim = dim
        self.bytes_per_tensor = seq_len * dim * 2 # FP16
        
    def simulate_baseline(self):
        # Baseline LayerNorm/RMSNorm requires 2 memory passes (read for variance, read/write for normalization)
        bandwidth = 100 * 1024**3 # 100 GB/s internal SRAM bandwidth
        latency = (self.bytes_per_tensor * 3) / bandwidth # Read + Read + Write
        return latency

    def simulate_flash_norm(self):
        # Hardware inline Flash-Norm calculates variance on the fly in register and normalizes in 1 pass
        bandwidth = 100 * 1024**3
        latency = (self.bytes_per_tensor * 2) / bandwidth # Read + Write
        return latency

def run_sim():
    print("Running Hardware Flash-Norm (HW-FlashNorm) Simulation...")
    sim = HW_FlashNorm()
    
    base_latency = sim.simulate_baseline()
    flash_latency = sim.simulate_flash_norm()
    
    speedup = base_latency / flash_latency if flash_latency > 0 else float('inf')
    
    print(f"Baseline Latency: {base_latency * 1000:.2f} ms")
    print(f"HW-FlashNorm Latency: {flash_latency * 1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    run_sim()
