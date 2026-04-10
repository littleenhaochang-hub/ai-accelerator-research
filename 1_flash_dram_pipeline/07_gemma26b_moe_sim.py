import math

print("=== Gemma-4 26B MoE: Extreme Edge Simulation ===")

# --- HARDWARE CONSTANTS ---
dram_bw_gbps = 50.0  
flash_bw_gbps = 3.0  
dram_energy_pj_per_byte = 45.0
flash_energy_pj_per_byte = 500.0  

# --- MODEL CONSTANTS (Hypothetical Gemma-4 26B MoE W4A4) ---
# Total Params = 26B. W4A4 = 13.0 GB Storage Footprint.
layers = 40
experts_per_layer = 64
active_experts_per_tok = 4

# Breakdown per layer:
# 1. Shared (Attention + Shared Expert) = 100 MB per layer
#    -> Total Shared = 40 * 100MB = 4.0 GB. (MUST be pinned in DRAM, otherwise Flash is too slow)
# 2. Experts = 64 experts * 3.5 MB = 224 MB per layer
#    -> Total Experts = 40 * 224MB = 8.96 GB.
layer_shared_mb = 100.0
expert_size_mb = 3.5
layer_active_experts_mb = expert_size_mb * active_experts_per_tok  # 14.0 MB

lookahead_accuracy = 0.80    

def get_hit_rate(num_pinned, total=64, s=1.2):
    if num_pinned >= total: return 1.0
    if num_pinned <= 0: return 0.0
    denom = sum([1.0 / (i ** s) for i in range(1, total + 1)])
    num = sum([1.0 / (i ** s) for i in range(1, num_pinned + 1)])
    return num / denom

def eval_26b_budget(expert_budget_gb):
    # Total AI RAM required = 4.0 GB (Shared) + Expert Budget
    expert_budget_mb = expert_budget_gb * 1024.0
    max_experts = math.floor(expert_budget_mb / expert_size_mb)
    pinned_per_layer = min(experts_per_layer, max_experts // layers)
    hit_rate = get_hit_rate(pinned_per_layer, total=experts_per_layer)
    
    # Per layer DRAM reads
    p3_dram_read = layer_shared_mb + (layer_active_experts_mb * hit_rate)
    p3_flash_read = layer_active_experts_mb * (1.0 - hit_rate)
    p3_flash_stall = p3_flash_read * (1.0 - lookahead_accuracy)
    p3_dram_write = p3_flash_read
    
    dram_time_ms = (p3_dram_read + p3_flash_read) / 1024.0 / dram_bw_gbps * 1000
    flash_stall_time_ms = (p3_flash_stall / 1024.0) / flash_bw_gbps * 1000
    layer_time_ms = dram_time_ms + flash_stall_time_ms
    token_time_ms = layer_time_ms * layers
    tps = 1000.0 / token_time_ms if token_time_ms > 0 else 0
    
    e_dram_read_mj = (p3_dram_read + p3_flash_read) * (1024**2) * dram_energy_pj_per_byte / 1e9
    e_flash_read_mj = p3_flash_read * (1024**2) * flash_energy_pj_per_byte / 1e9
    e_dram_write_mj = p3_dram_write * (1024**2) * dram_energy_pj_per_byte / 1e9
    token_energy_mj = (e_dram_read_mj + e_flash_read_mj + e_dram_write_mj) * layers
    
    total_ai_ram_gb = 4.0 + expert_budget_gb
    return total_ai_ram_gb, pinned_per_layer, hit_rate, tps, token_energy_mj, token_time_ms

expert_budgets = [0.0, 0.5, 1.0, 2.0, 4.0, 9.0]

print(f"| {'Total AI RAM':<12} | {'Pinned/Layer':<12} | {'Hit Rate':<10} | {'Tokens/sec':<10} | {'mJ/Token':<10} | {'Latency/Tk':<10} |")
print("|" + "-"*14 + "|" + "-"*14 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|")
for b in expert_budgets:
    ai_ram, p, hr, tps, mj, ms = eval_26b_budget(b)
    device_tier = ""
    if ai_ram <= 5.0: device_tier = "(8GB Phone)"
    elif ai_ram <= 9.0: device_tier = "(12GB Phone)"
    else: device_tier = "(16GB Flagship)"
        
    print(f"| {ai_ram:>4.1f} GB {device_tier:<12} | {p:>6} / 64 | {hr*100:>8.1f} % | {tps:>6.2f} T/s | {mj:>6.1f} mJ | {ms:>7.1f} ms |")

