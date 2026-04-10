import math

print("=== Gemma-4 26B A4B MoE: Extreme Edge Simulation ===")

# --- HARDWARE CONSTANTS ---
dram_bw_gbps = 50.0  
flash_bw_gbps = 3.0  
dram_energy_pj_per_byte = 45.0
flash_energy_pj_per_byte = 500.0  

# --- MODEL CONSTANTS: Gemma-4 26B A4B (W4A4 Compressed) ---
# Total Params = 25.2B. W4A4 (0.5 bytes/param) = 12.6 GB Total Footprint.
# Active Params = 3.8B. W4A4 = 1.9 GB Active Footprint.
layers = 30
total_experts_per_layer = 128
active_experts_per_tok = 8

# Parameter Breakdown (Approximate based on Gemma-4 configs):
# 1. Non-Expert (Vocab 256k*2816 + Attention QKVO): ~1.4B params -> 0.7 GB
# 2. Shared Expert: ~1.0B params -> 0.5 GB
# 3. Routed Experts: 25.2 - 1.4 - 1.0 = 22.8B params -> 11.4 GB
#    Per Layer Routed Experts = 11.4 GB / 30 = 389.1 MB
#    Per Expert = 389.1 MB / 128 = 3.04 MB
pinned_base_gb = 1.2  # 0.7GB (Attn/Embed) + 0.5GB (Shared)
expert_size_mb = 3.04
layer_active_experts_mb = expert_size_mb * active_experts_per_tok # ~24.3 MB

lookahead_accuracy = 0.80    

def get_hit_rate(num_pinned, total=128, s=1.2):
    if num_pinned >= total: return 1.0
    if num_pinned <= 0: return 0.0
    denom = sum([1.0 / (i ** s) for i in range(1, total + 1)])
    num = sum([1.0 / (i ** s) for i in range(1, num_pinned + 1)])
    return num / denom

def eval_gemma4_budget(total_ai_ram_gb):
    # We MUST pin the Base weights (1.2 GB)
    expert_budget_gb = total_ai_ram_gb - pinned_base_gb
    if expert_budget_gb < 0:
        expert_budget_gb = 0
        
    expert_budget_mb = expert_budget_gb * 1024.0
    max_experts = math.floor(expert_budget_mb / expert_size_mb)
    pinned_per_layer = min(total_experts_per_layer, max_experts // layers)
    hit_rate = get_hit_rate(pinned_per_layer, total=total_experts_per_layer)
    
    # Base read per layer (1.2GB / 30 = 40.96 MB)
    layer_base_mb = (pinned_base_gb * 1024) / layers
    
    # Per layer DRAM reads
    p3_dram_read = layer_base_mb + (layer_active_experts_mb * hit_rate)
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
    
    return total_ai_ram_gb, pinned_per_layer, hit_rate, tps, token_energy_mj, token_time_ms

expert_budgets = [2.0, 3.0, 4.0, 5.0, 8.0, 13.0]

print(f"| {'Total AI RAM':<12} | {'Pinned/Layer':<12} | {'Hit Rate':<10} | {'Tokens/sec':<10} | {'mJ/Token':<10} | {'Latency/Tk':<10} |")
print("|" + "-"*14 + "|" + "-"*14 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|")
for b in expert_budgets:
    ai_ram, p, hr, tps, mj, ms = eval_gemma4_budget(b)
    device_tier = ""
    if ai_ram <= 5.0: device_tier = "(8GB Phone)"
    elif ai_ram <= 8.0: device_tier = "(12GB Phone)"
    else: device_tier = "(16GB+ Flagship)"
        
    print(f"| {ai_ram:>4.1f} GB {device_tier:<12} | {p:>5} / 128 | {hr*100:>8.1f} % | {tps:>6.2f} T/s | {mj:>6.1f} mJ | {ms:>7.1f} ms |")

