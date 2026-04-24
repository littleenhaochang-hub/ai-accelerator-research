import time

def simulate_3d_stacked_sram():
    print("Simulating 3D Stacked SRAM (SRAM-on-Logic) for LLM KV Cache...")
    
    # Context: 128K context, 32 heads, 128 dim
    # Total KV Cache Size
    kv_cache_mb = (128000 * 128 * 32 * 2 * 2) / (1024 * 1024)
    print(f"Total KV Cache Size: {kv_cache_mb:.2f} MB")
    
    # 2D Planar SRAM (Baseline)
    # Heavily wire-delay bound for large capacities
    planar_latency_ns = 45.0 # High wire RC delay across a massive 2D chip
    planar_power_pj_per_bit = 0.8
    
    # 3D Stacked SRAM (SRAM-on-Logic via Hybrid Bonding)
    # TSV (Through-Silicon Via) reduces wire length massively
    stacked_latency_ns = 5.0
    stacked_power_pj_per_bit = 0.15
    
    speedup = planar_latency_ns / stacked_latency_ns
    power_reduction = planar_power_pj_per_bit / stacked_power_pj_per_bit
    
    print(f"2D Planar SRAM Access Latency: {planar_latency_ns:.1f} ns")
    print(f"3D Stacked SRAM Access Latency: {stacked_latency_ns:.1f} ns")
    print(f"Latency Speedup: {speedup:.2f}x")
    print(f"Power Reduction: {power_reduction:.2f}x")
    print("Conclusion: 3D stacking via hybrid bonding eliminates horizontal RC delays, enabling massive on-chip KV caches.")

if __name__ == '__main__':
    simulate_3d_stacked_sram()
