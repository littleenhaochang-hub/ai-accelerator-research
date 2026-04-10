import math

print("=== MoE DRAM Budget Sweep Simulation (1GB to 8GB) ===")

# --- HARDWARE CONSTANTS ---
layers = 24
dram_bw_gbps = 50.0  
flash_bw_gbps = 3.0  
dram_energy_pj_per_byte = 45.0
flash_energy_pj_per_byte = 500.0  

# --- MODEL CONSTANTS (W4A4 Compressed) ---
layer_full_mb = 272.0
layer_attn_shared_mb = 25.0
layer_active_experts_mb = 16.0
expert_size_mb = 3.5
experts_per_layer = 60
lookahead_accuracy = 0.80    

def get_hit_rate(num_pinned, total=60, s=1.2):
    if num_pinned >= total: return 1.0
    if num_pinned <= 0: return 0.0
    denom = sum([1.0 / (i ** s) for i in range(1, total + 1)])
    num = sum([1.0 / (i ** s) for i in range(1, num_pinned + 1)])
    return num / denom

def eval_budget(budget_gb):
    budget_mb = budget_gb * 1024.0
    max_experts = math.floor(budget_mb / expert_size_mb)
    pinned_per_layer = min(experts_per_layer, max_experts // layers)
    hit_rate = get_hit_rate(pinned_per_layer)
    
    p3_dram_read = layer_attn_shared_mb + (layer_active_experts_mb * hit_rate)
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
    
    return pinned_per_layer, hit_rate, tps, token_energy_mj, token_time_ms

budgets = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]

print(f"| {'DRAM Budget':<11} | {'Pinned/Layer':<12} | {'Hit Rate':<10} | {'Tokens/sec':<10} | {'mJ/Token':<10} | {'Latency/Tk':<10} |")
print("|" + "-"*13 + "|" + "-"*14 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*12 + "|")
for b in budgets:
    p, hr, tps, mj, ms = eval_budget(b)
    print(f"| {b:>7.1f} GB | {p:>7} / 60 | {hr*100:>8.1f} % | {tps:>6.2f} T/s | {mj:>6.1f} mJ | {ms:>7.1f} ms |")

