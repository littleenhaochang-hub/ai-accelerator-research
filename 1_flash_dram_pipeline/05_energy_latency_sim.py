import math

print("=== MoE Flash-DRAM Energy & Latency Simulation ===")

# --- HARDWARE CONSTANTS ---
layers = 24
dram_bw_gbps = 50.0  
flash_bw_gbps = 3.0  
dram_energy_pj_per_byte = 45.0
flash_energy_pj_per_byte = 500.0  # Assumption for UFS 4.0 Active Read (~1.5W at 3GB/s)

# --- MODEL CONSTANTS (Qwen1.5-MoE-A2.7B scale) ---
layer_full_mb = 1088.0
layer_active_total_mb = 164.0
layer_attn_shared_mb = 100.0
layer_active_experts_mb = 64.0

# --- ARCHITECTURE ASSUMPTIONS ---
dram_cache_hit_rate = 0.801   # 80.1% from LFU Pinning (1GB RAM)
lookahead_accuracy = 0.80     # 80% of Flash reads can be hidden by prefetch

def evaluate_architecture(name, dram_read_mb, flash_read_mb, flash_stall_mb, dram_write_mb=0):
    # Latency per layer
    dram_time_ms = (dram_read_mb / 1024.0) / dram_bw_gbps * 1000
    flash_stall_time_ms = (flash_stall_mb / 1024.0) / flash_bw_gbps * 1000
    layer_time_ms = dram_time_ms + flash_stall_time_ms
    token_time_ms = layer_time_ms * layers
    tps = 1000.0 / token_time_ms if token_time_ms > 0 else 0
    
    # Energy per layer
    e_dram_read_mj = dram_read_mb * (1024**2) * dram_energy_pj_per_byte / 1e9
    e_flash_read_mj = flash_read_mb * (1024**2) * flash_energy_pj_per_byte / 1e9
    e_dram_write_mj = dram_write_mb * (1024**2) * dram_energy_pj_per_byte / 1e9
    layer_energy_mj = e_dram_read_mj + e_flash_read_mj + e_dram_write_mj
    token_energy_mj = layer_energy_mj * layers
    
    return {
        "name": name,
        "layer_time_ms": layer_time_ms,
        "token_time_ms": token_time_ms,
        "tps": tps,
        "layer_energy_mj": layer_energy_mj,
        "token_energy_mj": token_energy_mj
    }

results = []

# 1. Baseline: Naive Flash Offload (Apple LLM in a flash without MoE optimization)
# Reads the entire 1088MB layer from Flash to DRAM, then reads from DRAM to compute.
res_naive = evaluate_architecture(
    "Baseline: Naive Flash Offload",
    dram_read_mb=layer_full_mb,
    flash_read_mb=layer_full_mb,
    flash_stall_mb=layer_full_mb,
    dram_write_mb=layer_full_mb
)
results.append(res_naive)

# 2. Our Architecture: Pillar 3 (Pinning + Lookahead Streaming)
# Attn/Shared (100MB) pinned in DRAM. Experts (64MB) -> 80.1% DRAM, 19.9% Flash.
# Lookahead hides 80% of Flash latency.
p3_dram_read = layer_attn_shared_mb + (layer_active_experts_mb * dram_cache_hit_rate)
p3_flash_read = layer_active_experts_mb * (1.0 - dram_cache_hit_rate)
p3_flash_stall = p3_flash_read * (1.0 - lookahead_accuracy)
p3_dram_write = p3_flash_read  # We must write the flash fetched experts to DRAM staging buffer

res_p3 = evaluate_architecture(
    "Proposed: MoE Pillar 3 (8GB Edge)",
    dram_read_mb=p3_dram_read,
    flash_read_mb=p3_flash_read,
    flash_stall_mb=p3_flash_stall,
    dram_write_mb=p3_dram_write
)
results.append(res_p3)

# 3. Upper Bound: Pure DRAM (16GB Flagship Phone)
# All 164MB active weights are in DRAM. No flash reads.
res_dram = evaluate_architecture(
    "Upper Bound: Pure DRAM (16GB+)",
    dram_read_mb=layer_active_total_mb,
    flash_read_mb=0,
    flash_stall_mb=0,
    dram_write_mb=0
)
results.append(res_dram)

print(f"{'Architecture':<40} | {'Tokens/sec':>10} | {'mJ/Token':>10} | {'Latency/Tk':>10}")
print("-" * 79)
for r in results:
    print(f"{r['name']:<40} | {r['tps']:>10.2f} | {r['token_energy_mj']:>10.1f} | {r['token_time_ms']:>8.1f} ms")

