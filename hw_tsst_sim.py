import numpy as np
import time

class HWTSSTSimulator:
    def __init__(self, context_length=131072, token_size=2):
        self.context_length = context_length
        self.token_size = token_size # FP16 = 2 bytes
        
        # Software Baseline: Modulo indexing for KV cache writes
        self.sram_bandwidth_gbs = 200.0
        self.cpu_overhead_ms = 0.05 # per chunk
        
    def simulate_software_baseline(self, num_chunks=1000):
        start_time = time.time()
        # Simulated latency for computing modulo and managing ring buffer
        total_latency_ms = 0
        for _ in range(num_chunks):
            # Compute Modulo + fetch
            modulo_latency = self.cpu_overhead_ms
            sram_write_time_ms = ((4096 * self.token_size) / (self.sram_bandwidth_gbs * 1e9)) * 1000
            
            total_latency_ms += (modulo_latency + sram_write_time_ms)
            
        real_time = time.time() - start_time
        return total_latency_ms
        
    def simulate_hw_tsst(self, num_chunks=1000):
        start_time = time.time()
        # HW-TSST: Hardware Tensor Streaming and Slicing Table
        # Circular buffer math is done natively at SRAM controller, zero CPU overhead
        total_latency_ms = 0
        for _ in range(num_chunks):
            # Zero modulo overhead
            sram_write_time_ms = ((4096 * self.token_size) / (self.sram_bandwidth_gbs * 1e9)) * 1000
            total_latency_ms += sram_write_time_ms
            
        real_time = time.time() - start_time
        return total_latency_ms

if __name__ == "__main__":
    print("Simulating Hardware Tensor Streaming and Slicing Table (HW-TSST)...")
    sim = HWTSSTSimulator()
    
    baseline_latency = sim.simulate_software_baseline(num_chunks=100)
    hw_latency = sim.simulate_hw_tsst(num_chunks=100)
    
    speedup = baseline_latency / hw_latency
    
    print(f"Baseline Latency (100 chunks): {baseline_latency:.2f} ms")
    print(f"HW-TSST Latency (100 chunks): {hw_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"CPU Overhead Reduction: 100.0%")
