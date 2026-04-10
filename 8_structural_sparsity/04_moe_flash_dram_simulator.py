import numpy as np

def simulate_moe_flash_dram_hierarchy():
    print("=== MoE Flash-DRAM Hierarchy Simulator ===")
    print("Hardware: 8GB DDR (1GB alloc for MoE Cache), 128GB UFS 4.0 Flash")
    
    # 1. Hardware & Model Parameters
    total_experts = 64
    expert_size_mb = 64.0 # 64MB per expert
    dram_cache_capacity_experts = 16 # Can hold 16 experts (1024 MB) in RAM
    
    flash_bw_gbps = 3.0 # Realistic UFS read speed
    dram_bw_gbps = 50.0 # LPDDR5x
    
    flash_read_ms = (expert_size_mb / 1024) / flash_bw_gbps * 1000
    dram_read_ms = (expert_size_mb / 1024) / dram_bw_gbps * 1000
    
    print(f"Expert Size: {expert_size_mb} MB")
    print(f"Flash Read Latency per Expert: {flash_read_ms:.2f} ms")
    print(f"DRAM Read Latency per Expert: {dram_read_ms:.2f} ms\n")

    # 2. Expert Pinning (LFU Cache) Simulation
    # Using Zipf's law to simulate expert activation frequencies (s=1.2)
    x = np.arange(1, total_experts + 1)
    frequencies = x**(-1.2)
    probabilities = frequencies / frequencies.sum()
    
    pinning_hit_rate = np.sum(probabilities[:dram_cache_capacity_experts])
    flash_miss_rate = 1.0 - pinning_hit_rate
    
    print("--- 1. Expert Pinning (LFU Cache) ---")
    print(f"Pinning Top {dram_cache_capacity_experts}/{total_experts} experts in DRAM.")
    print(f"DRAM Cache Hit Rate: {pinning_hit_rate*100:.1f}%")
    print(f"Flash Miss Rate: {flash_miss_rate*100:.1f}%")
    
    avg_latency_no_pinning = flash_read_ms # Assume all from flash initially
    avg_latency_with_pinning = (pinning_hit_rate * dram_read_ms) + (flash_miss_rate * flash_read_ms)
    print(f"Avg Latency (No Pinning, purely Flash): {avg_latency_no_pinning:.2f} ms")
    print(f"Avg Latency (With Pinning): {avg_latency_with_pinning:.2f} ms\n")

    # 3. Lookahead Routing Simulation
    # Apply lookahead only to the Flash misses
    print("--- 2. Lookahead Routing (Prefetching) ---")
    lookahead_accuracy = 0.80 # 80% accuracy in predicting Layer N+1 expert at Layer N
    
    # If Lookahead is correct: Flash read is hidden behind compute. Latency = DRAM read time (from staging buffer)
    # If Lookahead is wrong: Pipeline stalls, must read from Flash synchronously.
    hidden_reads = flash_miss_rate * lookahead_accuracy
    stalled_reads = flash_miss_rate * (1.0 - lookahead_accuracy)
    
    print(f"Lookahead Accuracy: {lookahead_accuracy*100:.1f}%")
    print(f"Effectively Hidden Flash Reads: {hidden_reads*100:.1f}% of total tokens")
    print(f"Remaining Pipeline Stalls (Flash Reads): {stalled_reads*100:.1f}% of total tokens")
    
    final_avg_latency = (pinning_hit_rate * dram_read_ms) + (hidden_reads * dram_read_ms) + (stalled_reads * flash_read_ms)
    
    print(f"\n=== Final System Performance ===")
    print(f"Base MoE (Pure Flash): {flash_read_ms:.2f} ms / layer")
    print(f"Optimized MoE (Pinning + Lookahead): {final_avg_latency:.2f} ms / layer")
    print(f"Hardware Speedup: {flash_read_ms / final_avg_latency:.2f}x")

simulate_moe_flash_dram_hierarchy()
