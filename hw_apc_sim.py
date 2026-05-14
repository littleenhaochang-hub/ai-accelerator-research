import time

def simulate_software_prefix_caching(seq_len):
    # Radix tree lookup in software + DRAM fetch
    lookup_latency = 0.015 # 15ms CPU overhead
    dram_latency = (seq_len * 2) / 1e9 # KV fetch
    return lookup_latency + dram_latency

def simulate_hardware_apc(seq_len):
    # Hardware TCAM lookup + SRAM direct map
    lookup_latency = 0.0005 # 500us TCAM overhead
    sram_latency = (seq_len * 2) / 1e10 # Much faster SRAM mapping
    return lookup_latency + sram_latency

if __name__ == "__main__":
    seq_len = 65536 # 64K agent prompt
    
    soft_time = simulate_software_prefix_caching(seq_len)
    hw_time = simulate_hardware_apc(seq_len)
    
    print(f"Software Prefix Caching Latency: {soft_time:.4f} s")
    print(f"HW-APC TCAM Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
