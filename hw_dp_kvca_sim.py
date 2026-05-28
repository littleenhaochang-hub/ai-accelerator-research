import time

class HWDPKVCASimulator:
    def __init__(self, context_length=131072, hidden_dim=4096, num_layers=32):
        self.context_length = context_length
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.sram_bw_gbs = 200.0 # GB/s internal SRAM bandwidth
        
    def simulate_baseline_fp16(self):
        # Baseline: All tokens stored in FP16 (2 bytes)
        bytes_per_token = 2
        total_kv_cache_bytes = self.context_length * self.hidden_dim * self.num_layers * bytes_per_token * 2 # K and V
        total_kv_mb = total_kv_cache_bytes / (1024 * 1024)
        
        # Read latency per step
        latency_ms = (total_kv_mb / 1024) / self.sram_bw_gbs * 1000
        return total_kv_mb, latency_ms

    def simulate_hw_dp_kvca(self, heavy_hitter_ratio=0.10):
        # HW-DP-KVCA: 10% Heavy Hitters in FP8 (1 byte), 90% background in 2-bit (0.25 bytes)
        # Hardware dynamically manages the paging and on-the-fly decompression
        heavy_hitters = self.context_length * heavy_hitter_ratio
        background = self.context_length * (1 - heavy_hitter_ratio)
        
        bytes_per_heavy = 1.0 # FP8
        bytes_per_bg = 0.25 # 2-bit
        
        total_kv_cache_bytes = (heavy_hitters * bytes_per_heavy + background * bytes_per_bg) * self.hidden_dim * self.num_layers * 2
        total_kv_mb = total_kv_cache_bytes / (1024 * 1024)
        
        # Read latency per step
        latency_ms = (total_kv_mb / 1024) / self.sram_bw_gbs * 1000
        return total_kv_mb, latency_ms

if __name__ == "__main__":
    print("Simulating Hardware Dynamic Precision KV Cache Allocator (HW-DP-KVCA)...")
    sim = HWDPKVCASimulator()
    
    base_mb, base_lat = sim.simulate_baseline_fp16()
    hw_mb, hw_lat = sim.simulate_hw_dp_kvca(heavy_hitter_ratio=0.10)
    
    print(f"Baseline FP16 KV Cache (128K ctx): {base_mb:.2f} MB, Fetch Latency: {base_lat:.2f} ms")
    print(f"HW-DP-KVCA KV Cache (128K ctx): {hw_mb:.2f} MB, Fetch Latency: {hw_lat:.2f} ms")
    print(f"Memory Reduction: {(base_mb - hw_mb) / base_mb * 100:.2f}%")
    print(f"Speedup: {base_lat / hw_lat:.2f}x")
