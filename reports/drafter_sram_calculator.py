import math

def calculate_drafter_sram_requirements(model_params_billions=0.5, precision_bits=4, max_context_length=8192, hidden_size=1024, num_layers=24):
    """
    Calculates the required SRAM (in Megabytes) to hold a Drafter model entirely on-chip.
    This eliminates DRAM bandwidth bottlenecks completely for the draft phase.
    """
    
    # 1. Weights (Model Parameters)
    # Total bits = parameters * bits_per_param
    weights_bits = (model_params_billions * 1e9) * precision_bits
    weights_bytes = weights_bits / 8
    weights_mb = weights_bytes / (1024 * 1024)
    
    # Add overhead for Block 32 sub-channel scaling factors (if W4A4 Block 32 is used)
    # Every 32 elements share a 16-bit scale -> effectively adds 0.5 bits per parameter
    if precision_bits == 4:
        scale_overhead_bits = (model_params_billions * 1e9) * (16 / 32)
        scale_overhead_mb = (scale_overhead_bits / 8) / (1024 * 1024)
        weights_mb += scale_overhead_mb

    # 2. KV Cache (Dynamic Memory)
    # KV Cache Size = 2 (K and V) * seq_len * hidden_size * num_layers * precision_bits
    # Assuming A4KV4 (4-bit KV Cache)
    kv_cache_bits = 2 * max_context_length * hidden_size * num_layers * precision_bits
    kv_cache_bytes = kv_cache_bits / 8
    kv_cache_mb = kv_cache_bytes / (1024 * 1024)
    
    # Add overhead for KV Cache scaling factors (Assuming group size 128 for KV)
    kv_scale_overhead_bits = (kv_cache_bits / precision_bits) * (16 / 128)
    kv_scale_overhead_mb = (kv_scale_overhead_bits / 8) / (1024 * 1024)
    kv_cache_mb += kv_scale_overhead_mb

    # 3. Activations & Buffers (Temporary working memory per layer)
    # Batch size = 1 during draft generation. Very small footprint.
    # Just need enough to hold Q, K, V, and intermediate FFN states for one token.
    # Usually < 1 MB for a 0.5B model. We'll allocate a generous 2 MB buffer.
    activation_buffer_mb = 2.0 

    total_sram_mb = weights_mb + kv_cache_mb + activation_buffer_mb

    print(f"--- Drafter SRAM Requirements ({model_params_billions}B Model, {precision_bits}-bit) ---")
    print(f"Weights (including scales): {weights_mb:.2f} MB")
    print(f"KV Cache (Context: {max_context_length}): {kv_cache_mb:.2f} MB")
    print(f"Activation Buffers:         {activation_buffer_mb:.2f} MB")
    print(f"--------------------------------------------------")
    print(f"Total Minimum SRAM Required: {total_sram_mb:.2f} MB\n")
    return total_sram_mb

# Test typical Drafter sizes (e.g., 68M, 135M, 500M parameters) at W4A4
print("Scenario 1: Ultra-Small Drafter (e.g., LLaMA-68M architecture)")
calculate_drafter_sram_requirements(model_params_billions=0.068, precision_bits=4, max_context_length=8192, hidden_size=512, num_layers=12)

print("Scenario 2: Medium Drafter (e.g., 135M parameters)")
calculate_drafter_sram_requirements(model_params_billions=0.135, precision_bits=4, max_context_length=8192, hidden_size=768, num_layers=12)

print("Scenario 3: Standard 0.5B Drafter (like our Qwen2.5-0.5B)")
calculate_drafter_sram_requirements(model_params_billions=0.5, precision_bits=4, max_context_length=8192, hidden_size=1024, num_layers=24)


# Add edge device scenarios (Smartphones like Snapdragon 8 Gen 4 / Apple A19)
print("\n=== Smartphone Scenarios (LPDDR5x / Limited SRAM) ===")
# Smartphones typically have 8MB-16MB L2/L3 Cache (System Level Cache)
# We need to squeeze the Drafter into extremely tight budgets (e.g. 10M to 30M params)

print("Scenario 4: Nano-Drafter (e.g., 30M params, 2K Context)")
# 30M param, 256 hidden size, 8 layers
calculate_drafter_sram_requirements(model_params_billions=0.030, precision_bits=4, max_context_length=2048, hidden_size=256, num_layers=8)

print("Scenario 5: Micro-Drafter (e.g., 10M params, 1K Context)")
# 10M param, 128 hidden size, 4 layers
calculate_drafter_sram_requirements(model_params_billions=0.010, precision_bits=4, max_context_length=1024, hidden_size=128, num_layers=4)
