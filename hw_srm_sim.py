import time

def simulate_hw_srm(query_groups=64, kv_length=32768):
    # Baseline: Software pointer tracking for GQA creates memory fragmentation
    # fetching the same Key/Value for multiple queries via software replication
    software_latency_ms = query_groups * 0.05 
    
    # Proposed: Hardware SRAM Replication Multiplexer (HW-SRM)
    # Replicates KV pairs across the SRAM output bus to multiple MAC arrays in zero cycles
    hardware_latency_ms = 0.002 # just the multicast setup time
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Query Groups: {query_groups}, KV Length: {kv_length}")
    print(f"Baseline Latency (Software GQA replication): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SRM): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_srm()
