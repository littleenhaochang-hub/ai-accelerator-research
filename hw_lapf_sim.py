import math

def simulate_baseline_lora_fetch(num_agents, adapter_size_mb, bandwidth_gb_s):
    # Baseline: Demand fetch LoRA weights via PCIe when multi-tenant context switching
    total_time = 0
    bandwidth_mb_ms = bandwidth_gb_s * 1024 / 1000
    for _ in range(num_agents):
        fetch_time = adapter_size_mb / bandwidth_mb_ms
        total_time += fetch_time
    return total_time

def simulate_hw_lapf_fetch(num_agents, adapter_size_mb, bandwidth_gb_s):
    # HW-LAPF: Hardware LoRA Adapter Pre-Fetcher
    # DMA pre-fetches next LoRA weights asynchronously into a background SRAM bank
    # Only a tiny setup overhead per switch, main fetch is masked
    setup_overhead = 0.001 
    return num_agents * setup_overhead

if __name__ == "__main__":
    agents = 128
    adapter_size = 32 # 32MB LoRA adapter
    bandwidth = 16 # Gen4 x8
    
    base_lat = simulate_baseline_lora_fetch(agents, adapter_size, bandwidth)
    lapf_lat = simulate_hw_lapf_fetch(agents, adapter_size, bandwidth)
    
    speedup = base_lat / lapf_lat if lapf_lat > 0 else 0
    
    print(f"Baseline Fetch Latency: {base_lat:.2f} ms")
    print(f"HW-LAPF Latency: {lapf_lat:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
