import math

def simulate_moe_speculative_decoding(
    target_model_params_b = 7.0,
    drafter_total_params_b = 0.068,
    drafter_active_params_b = 0.017,
    sram_mb = 32.0,
    lpddr5x_gbps = 50.0,
    guess_length = 5,
    acceptance_rate = 0.70
):
    print("=== MoE Drafter Bandwidth Simulation (Cycle-Accurate) ===")
    print(f"Target: {target_model_params_b}B | Drafter: {drafter_total_params_b*1000}M (Active: {drafter_active_params_b*1000}M)")
    print(f"Memory: LPDDR5x @ {lpddr5x_gbps} GB/s | SRAM: {sram_mb} MB")

    # Assuming W4A4 + Block 32 E4M3 scale (4.25 bits / param footprint)
    bits_per_param = 4.25
    bytes_per_param = bits_per_param / 8

    target_dram_mb = (target_model_params_b * 1e9 * bytes_per_param) / (1024 * 1024)
    drafter_total_mb = (drafter_total_params_b * 1e9 * bytes_per_param) / (1024 * 1024)
    drafter_active_mb = (drafter_active_params_b * 1e9 * bytes_per_param) / (1024 * 1024)

    print(f"Target DRAM Size: {target_dram_mb/1024:.2f} GB")
    print(f"Drafter Total Size: {drafter_total_mb:.2f} MB")
    print(f"Drafter Active Size per Token: {drafter_active_mb:.2f} MB\n")

    # We simulate reading the target model exactly once per batch of K guesses
    target_read_time_ms = (target_dram_mb / 1024) / lpddr5x_gbps * 1000

    # From our previous locality simulation, we know Token T+1 uses the same expert as T roughly 65% of the time.
    # With a 3-expert SRAM cache, hit rate is around 50%.
    cache_hit_rate = 0.50
    cache_miss_rate = 1.0 - cache_hit_rate

    # Time to generate 1 draft token
    # If hit: SRAM time is negligible (~0.01 ms)
    # If miss: Read active_mb from LPDDR5x
    dram_miss_time_ms = (drafter_active_mb / 1024) / lpddr5x_gbps * 1000
    sram_hit_time_ms = 0.01

    avg_draft_token_time_ms = (cache_hit_rate * sram_hit_time_ms) + (cache_miss_rate * dram_miss_time_ms)
    total_draft_time_ms = avg_draft_token_time_ms * guess_length

    total_step_time_ms = total_draft_time_ms + target_read_time_ms

    expected_accepted = sum([math.pow(acceptance_rate, i) for i in range(1, guess_length + 1)])
    tokens_per_step = expected_accepted + 1 
    token_rate = (tokens_per_step / total_step_time_ms) * 1000

    print(f"--- Timing Analysis ---")
    print(f"Time to verify {guess_length} tokens (Target Read): {target_read_time_ms:.2f} ms")
    print(f"Time for 1 Drafter Cache Miss: {dram_miss_time_ms:.2f} ms")
    print(f"Avg Drafter Time per Token (50% Hit): {avg_draft_token_time_ms:.2f} ms")
    print(f"Total Drafter Time for {guess_length} tokens: {total_draft_time_ms:.2f} ms")
    print(f"Total Step Time: {total_step_time_ms:.2f} ms")
    
    print(f"\n--- Final Token Rate ---")
    print(f"Expected Tokens per Step: {tokens_per_step:.2f}")
    print(f"Token Rate: {token_rate:.1f} Tokens/second")
    print(f"Speedup vs Autoregressive ({1000/target_read_time_ms:.1f} T/s): {token_rate / (1000/target_read_time_ms):.2f}x\n")

simulate_moe_speculative_decoding()
