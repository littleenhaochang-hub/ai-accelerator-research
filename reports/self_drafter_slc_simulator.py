import math

def simulate_self_drafter_cache_dynamics(
    main_model_b=7.0, 
    total_layers=32, 
    draft_layers_count=6, # e.g., using first 3 and last 3 layers as drafter
    slc_capacity_mb=32.0, 
    dram_bw_gbps=128.0, 
    slc_bw_gbps=256.0,
    guess_length=5,
    precision_bits=4
):
    # 1. Model Sizes in GB
    total_weight_gb = (main_model_b * 1e9 * precision_bits / 8) / 1e9
    weight_per_layer_mb = (total_weight_gb * 1024) / total_layers
    draft_weight_mb = weight_per_layer_mb * draft_layers_count

    print("=== Hardware & Self-Drafter Specs ===")
    print(f"SLC Capacity: {slc_capacity_mb} MB")
    print(f"Total Model ({main_model_b}B, {total_layers} layers): {total_weight_gb*1024:.0f} MB")
    print(f"Self-Drafter Subset ({draft_layers_count} layers): {draft_weight_mb:.0f} MB\n")

    # 2. SLC Thrashing Analysis
    print("=== Cache Thrashing Analysis (Decode Phase) ===")
    if draft_weight_mb > slc_capacity_mb:
        print(f"[FAIL] The Draft layers ({draft_weight_mb:.0f} MB) are TOO LARGE for the {slc_capacity_mb} MB SLC.")
        print(f"       Every draft step will cause DRAM traffic and wipe the SLC.")
    else:
        print(f"[PASS] The Draft layers fit in SLC! High locality achieved.")

    # 3. Token Rate Calculation (Decode)
    # Draft Phase: Generating K tokens sequentially using the subset of layers
    if draft_weight_mb > slc_capacity_mb:
        # Must read from DRAM
        draft_time_per_token_ms = (draft_weight_mb / 1024) / dram_bw_gbps * 1000
        draft_memory_source = "DRAM"
    else:
        draft_time_per_token_ms = (draft_weight_mb / 1024) / slc_bw_gbps * 1000
        draft_memory_source = "SLC"

    total_draft_time_ms = draft_time_per_token_ms * guess_length

    # Verify Phase: Reading the FULL model from DRAM
    verify_time_ms = total_weight_gb / dram_bw_gbps * 1000

    # Total time
    total_time_ms = total_draft_time_ms + verify_time_ms

    # Let's assume 70% acceptance rate for K=5 -> ~2.9 tokens accepted + 1 = 3.9 tokens
    expected_tokens = 3.9 
    token_rate = (expected_tokens / total_time_ms) * 1000

    print(f"\n=== Decode Performance Simulation ===")
    print(f"Draft Phase ({guess_length} tokens from {draft_memory_source}): {total_draft_time_ms:.2f} ms")
    print(f"Verify Phase (Full Model from DRAM): {verify_time_ms:.2f} ms")
    print(f"Total Time per Step: {total_time_ms:.2f} ms")
    print(f"Token Rate: {token_rate:.1f} Tokens/second")

    # Compare to Baseline
    baseline_time = verify_time_ms # Just reading full model once per token
    baseline_rate = 1000 / baseline_time
    print(f"\nBaseline (No Drafter): {baseline_rate:.1f} Tokens/second")
    print(f"Speedup: {token_rate/baseline_rate:.2f}x")

simulate_self_drafter_cache_dynamics()
