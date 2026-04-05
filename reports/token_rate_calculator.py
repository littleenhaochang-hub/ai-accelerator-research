import math

def simulate_edge_hardware(main_model_b=7.0, drafter_model_b=0.030, 
                           dram_bw_gbps=128.0, slc_bw_gbps=256.0, 
                           slc_capacity_mb=32.0, guess_length=5, acceptance_rate=0.7):
                           
    print(f"=== Hardware Specs ===")
    print(f"DRAM: 4GB Capacity | {dram_bw_gbps} GB/s Bandwidth")
    print(f"SLC:  {slc_capacity_mb}MB Capacity | {slc_bw_gbps} GB/s Bandwidth\n")

    # 1. Main Model Specs (Assuming 4-bit weights)
    main_weight_gb = (main_model_b * 1e9 * 4 / 8) / 1e9
    print(f"Main Model ({main_model_b}B, 4-bit): {main_weight_gb:.2f} GB")
    if main_weight_gb * 1024 > slc_capacity_mb:
        print(f" -> Result: Main Model MUST run from DRAM.\n")
        
    # 2. Drafter Model Specs (Assuming 4-bit weights)
    drafter_weight_mb = (drafter_model_b * 1e9 * 4 / 8) / (1024 * 1024)
    print(f"Drafter Model ({drafter_model_b*1000}M, 4-bit): {drafter_weight_mb:.2f} MB")
    if drafter_weight_mb <= slc_capacity_mb:
        print(f" -> Result: Drafter perfectly fits in SLC! Zero DRAM access.\n")

    # --- BASELINE: Standard Autoregressive (No Drafter) ---
    # Generating 1 token requires reading the entire Main Model from DRAM once.
    time_per_token_ar = main_weight_gb / dram_bw_gbps
    token_rate_ar = 1 / time_per_token_ar
    
    print(f"=== 1. Standard Autoregressive (Main Model Only) ===")
    print(f"Time to read {main_weight_gb:.2f} GB from DRAM: {time_per_token_ar*1000:.1f} ms")
    print(f"Token Rate: {token_rate_ar:.1f} Tokens/second\n")

    # --- SPECULATIVE DECODING: Drafter + Main Model ---
    # Step A: Drafter guesses K tokens from SLC
    drafter_time_per_token = (drafter_weight_mb / 1024) / slc_bw_gbps
    drafter_time_total = drafter_time_per_token * guess_length
    
    # Step B: Main Model verifies K tokens in parallel
    # Crucial Physics: Verifying 5 tokens in parallel (Batch=5) takes the EXACT SAME memory bandwidth as generating 1 token!
    main_verify_time = main_weight_gb / dram_bw_gbps
    
    # Expected Tokens generated = Expected accepted + 1 (the correction token)
    # E[tokens] = sum(p^i) from i=1 to K
    expected_accepted = sum([math.pow(acceptance_rate, i) for i in range(1, guess_length + 1)])
    total_generated_per_step = expected_accepted + 1 
    
    total_time_per_step = drafter_time_total + main_verify_time
    token_rate_spec = total_generated_per_step / total_time_per_step
    
    speedup = token_rate_spec / token_rate_ar

    print(f"=== 2. Speculative Decoding (Drafter guesses {guess_length} tokens) ===")
    print(f"Step A (Drafter in SLC): Guess {guess_length} tokens takes {drafter_time_total*1000:.2f} ms")
    print(f"Step B (Main in DRAM):   Verify {guess_length} tokens takes {main_verify_time*1000:.1f} ms")
    print(f"Total Time per Step:     {total_time_per_step*1000:.1f} ms")
    print(f"Average Tokens Gained:   {total_generated_per_step:.1f} tokens (Assuming {acceptance_rate*100}% hit rate)")
    print(f"Token Rate:              {token_rate_spec:.1f} Tokens/second")
    print(f"SPEEDUP:                 {speedup:.2f}x\n")

simulate_edge_hardware()
