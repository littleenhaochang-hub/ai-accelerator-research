import time

def simulate_demand_lora_fetch(adapter_size_mb):
    # Fetch LoRA weights from DRAM/NVMe on demand
    latency = 0.005 # 5ms blocking overhead per context switch
    transfer = adapter_size_mb / 64000.0
    return latency + transfer

def simulate_hw_lapf_prefetch(adapter_size_mb):
    # Hardware lookahead prefetcher into SRAM
    hardware_overhead = 0.0001 # 100us scheduling overhead
    # Transfer is hidden behind previous token compute
    return hardware_overhead

if __name__ == "__main__":
    adapter_size = 32 # 32MB LoRA adapter
    num_switches = 100 # Multi-tenant batching
    
    demand_time = sum([simulate_demand_lora_fetch(adapter_size) for _ in range(num_switches)])
    prefetch_time = sum([simulate_hw_lapf_prefetch(adapter_size) for _ in range(num_switches)])
    
    print(f"Demand LoRA Fetch Latency: {demand_time:.4f} s")
    print(f"HW-LAPF Prefetch Latency: {prefetch_time:.4f} s")
    print(f"Speedup: {demand_time / prefetch_time:.2f}x")
