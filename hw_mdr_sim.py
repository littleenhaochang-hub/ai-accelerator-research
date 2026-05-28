import time

class HWMDRSimulator:
    def __init__(self, expert_size_fp16_mb=256, num_experts_fetched=4):
        self.expert_size_fp16_mb = expert_size_fp16_mb
        self.num_experts_fetched = num_experts_fetched
        
        self.pcie_gen5_bw_gbs = 64.0 # GB/s
        self.sram_bw_gbs = 200.0 # GB/s
        
    def simulate_baseline_moe(self, tokens=1000):
        # Baseline: Fetch full FP16 experts from NVMe/DRAM over PCIe
        total_latency_ms = 0
        for _ in range(tokens):
            fetch_volume_mb = self.expert_size_fp16_mb * self.num_experts_fetched
            fetch_latency = (fetch_volume_mb / 1024) / self.pcie_gen5_bw_gbs * 1000 # ms
            total_latency_ms += fetch_latency
        return total_latency_ms
        
    def simulate_hw_mdr(self, tokens=1000):
        # HW-MDR: Base expert pinned in SRAM. Fetch only 2-bit Deltas for specific experts.
        # Hardware reconstructs Expert = Base + Delta on-the-fly.
        delta_compression_ratio = 16.0 / 2.0 # FP16 to 2-bit
        total_latency_ms = 0
        for _ in range(tokens):
            fetch_volume_mb = (self.expert_size_fp16_mb / delta_compression_ratio) * self.num_experts_fetched
            fetch_latency = (fetch_volume_mb / 1024) / self.pcie_gen5_bw_gbs * 1000 # ms
            total_latency_ms += fetch_latency
        return total_latency_ms

if __name__ == "__main__":
    print("Simulating Hardware MoE Delta Reconstructor (HW-MDR)...")
    sim = HWMDRSimulator()
    
    base_lat = sim.simulate_baseline_moe(tokens=100)
    hw_lat = sim.simulate_hw_mdr(tokens=100)
    
    speedup = base_lat / hw_lat
    bw_reduction = (1 - (hw_lat / base_lat)) * 100
    
    print(f"Baseline Fetch Latency (100 tokens): {base_lat:.2f} ms")
    print(f"HW-MDR Latency (100 tokens): {hw_lat:.2f} ms")
    print(f"Latency Speedup: {speedup:.2f}x")
    print(f"PCIe Bandwidth Reduction: {bw_reduction:.2f}%")
