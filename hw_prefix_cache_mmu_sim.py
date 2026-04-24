import time

def sw_prefix_cache_lookup(num_requests):
    # Simulated latency for software Radix Tree lookup for Prefix Caching
    latency = num_requests * 0.5 # ms
    return latency

def hw_mmu_prefix_cache_lookup(num_requests):
    # Simulated latency for Hardware MMU Page Table Walker
    latency = num_requests * 0.02 # ms
    return latency

def main():
    num_requests = 1000
    print("Running Hardware Prefix Caching MMU Simulation...")
    sw_lat = sw_prefix_cache_lookup(num_requests)
    print(f"Software Radix Tree Latency: {sw_lat:.2f} ms")
    
    hw_lat = hw_mmu_prefix_cache_lookup(num_requests)
    print(f"Hardware MMU Walker Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
