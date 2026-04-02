import math

def calculate_moe_drafter_sram(total_params_b=0.068, active_params_b=0.017, precision_bits=4, max_context_length=2048, hidden_size=256, num_layers=8, cache_lines=2):
    """
    Calculates SRAM for an MoE Drafter.
    total_params: Total size of the model (e.g. 4 experts)
    active_params: Parameters activated per token (e.g. 1 expert)
    """
    # 1. Weights (Total vs Active)
    total_weights_mb = (total_params_b * 1e9 * precision_bits / 8) / (1024 * 1024)
    active_weights_mb = (active_params_b * 1e9 * precision_bits / 8) / (1024 * 1024)
    
    if precision_bits == 4:
        total_scale_mb = ((total_params_b * 1e9 * (16/32)) / 8) / (1024 * 1024)
        active_scale_mb = ((active_params_b * 1e9 * (16/32)) / 8) / (1024 * 1024)
        total_weights_mb += total_scale_mb
        active_weights_mb += active_scale_mb

    # 2. KV Cache
    kv_cache_bits = 2 * max_context_length * hidden_size * num_layers * precision_bits
    kv_cache_mb = (kv_cache_bits / 8) / (1024 * 1024)
    if precision_bits == 4:
        kv_cache_mb += ((kv_cache_bits/4)*(16/128)/8) / (1024 * 1024)

    # 3. Dynamic Expert Cache (SRAM Locality Buffer)
    # How much SRAM do we dedicate to holding "recently used" or "prefetched" experts?
    # E.g., keeping 2 out of 4 experts in SRAM at all times.
    expert_cache_mb = active_weights_mb * cache_lines

    print(f"--- MoE Drafter: {total_params_b*1000:.0f}M Total / {active_params_b*1000:.0f}M Active ({precision_bits}-bit) ---")
    print(f"Total Model Footprint (DRAM): {total_weights_mb:.2f} MB")
    print(f"KV Cache (SRAM):              {kv_cache_mb:.2f} MB")
    print(f"Single Token Active Weights:  {active_weights_mb:.2f} MB")
    print(f"Expert Cache (SRAM Buffer):   {expert_cache_mb:.2f} MB (Holds {cache_lines} expert paths)")
    print(f"--------------------------------------------------")
    total_sram = kv_cache_mb + expert_cache_mb + 2.0 # 2MB activation buffer
    print(f"Target SRAM Allocation:       {total_sram:.2f} MB\n")

# Scenario A: 4-Expert MoE on Smartphone (e.g. 68M total, 17M active)
calculate_moe_drafter_sram(total_params_b=0.068, active_params_b=0.017, precision_bits=4, max_context_length=2048, hidden_size=256, num_layers=8, cache_lines=2)

# Scenario B: 8-Expert MoE on Smartphone (e.g. 136M total, 17M active)
calculate_moe_drafter_sram(total_params_b=0.136, active_params_b=0.017, precision_bits=4, max_context_length=2048, hidden_size=256, num_layers=8, cache_lines=3)
