import math

def simulate_drafter_location(main_model_b=7.0, drafter_small_b=0.030, drafter_large_b=0.5,
                              dram_bw_gbps=128.0, slc_bw_gbps=256.0, 
                              dram_latency_ms=0.5, slc_latency_ms=0.02, # Real-world edge latencies
                              guess_length=5, acceptance_rate=0.7):
                              
    # Model Sizes in GB (4-bit)
    main_gb = (main_model_b * 1e9 * 4 / 8) / 1e9
    draft_small_gb = (drafter_small_b * 1e9 * 4 / 8) / 1e9
    draft_large_gb = (drafter_large_b * 1e9 * 4 / 8) / 1e9
    
    # Expected generated tokens per step
    E_tokens = sum([math.pow(acceptance_rate, i) for i in range(1, guess_length + 1)])
    total_tokens_per_step = E_tokens + 1

    # Time to read Main Model from DRAM once (Verification)
    main_dram_time_ms = (main_gb / dram_bw_gbps) * 1000 + dram_latency_ms

    print("=== Edge Hardware Physics ===")
    print(f"Main Model (7B, 4-bit): {main_gb*1024:.0f} MB")
    print(f"Small Drafter (30M):    {draft_small_gb*1024:.1f} MB (Fits in SLC)")
    print(f"Large Drafter (0.5B):   {draft_large_gb*1024:.0f} MB (Forced to DRAM)\n")

    # 1. Baseline (No Drafter)
    token_rate_baseline = 1000 / main_dram_time_ms
    print(f"[1] Baseline: No Drafter (Main in DRAM)")
    print(f"    Time per token: {main_dram_time_ms:.2f} ms")
    print(f"    Token Rate:     {token_rate_baseline:.1f} tokens/s\n")

    # 2. Small Drafter in SLC
    # Generation takes K steps of SLC reads
    draft_step_time_slc = (draft_small_gb / slc_bw_gbps) * 1000 + slc_latency_ms
    draft_total_time_slc = draft_step_time_slc * guess_length
    total_time_slc = draft_total_time_slc + main_dram_time_ms
    rate_slc = (total_tokens_per_step / total_time_slc) * 1000
    
    print(f"[2] Small Drafter in SLC (256 GB/s + Low Latency)")
    print(f"    Drafter time ({guess_length} tokens): {draft_total_time_slc:.2f} ms ({draft_step_time_slc:.2f}ms/token)")
    print(f"    Main Verify time:       {main_dram_time_ms:.2f} ms")
    print(f"    Token Rate:             {rate_slc:.1f} tokens/s (Speedup: {rate_slc/token_rate_baseline:.2f}x)\n")

    # 3. Small Drafter in DRAM
    draft_step_time_dram = (draft_small_gb / dram_bw_gbps) * 1000 + dram_latency_ms
    draft_total_time_dram = draft_step_time_dram * guess_length
    total_time_dram = draft_total_time_dram + main_dram_time_ms
    rate_dram = (total_tokens_per_step / total_time_dram) * 1000
    
    print(f"[3] Small Drafter in DRAM (128 GB/s + High Latency Contention)")
    print(f"    Drafter time ({guess_length} tokens): {draft_total_time_dram:.2f} ms ({draft_step_time_dram:.2f}ms/token)")
    print(f"    Main Verify time:       {main_dram_time_ms:.2f} ms")
    print(f"    Token Rate:             {rate_dram:.1f} tokens/s (Speedup: {rate_dram/token_rate_baseline:.2f}x)\n")
    
    # 4. Large Drafter in DRAM
    draft_large_step_time = (draft_large_gb / dram_bw_gbps) * 1000 + dram_latency_ms
    draft_large_total_time = draft_large_step_time * guess_length
    total_time_large_dram = draft_large_total_time + main_dram_time_ms
    rate_large_dram = (total_tokens_per_step / total_time_large_dram) * 1000
    
    print(f"[4] Large 0.5B Drafter in DRAM (Typical setup without extreme quantization)")
    print(f"    Drafter time ({guess_length} tokens): {draft_large_total_time:.2f} ms ({draft_large_step_time:.2f}ms/token)")
    print(f"    Main Verify time:       {main_dram_time_ms:.2f} ms")
    print(f"    Token Rate:             {rate_large_dram:.1f} tokens/s (Speedup: {rate_large_dram/token_rate_baseline:.2f}x)\n")

simulate_drafter_location()
