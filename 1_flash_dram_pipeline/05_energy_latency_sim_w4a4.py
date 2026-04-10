import math

print("=== MoE Flash-DRAM Energy & Latency Simulation (W4A4 + Layer-wise Pinning) ===")

# --- HARDWARE CONSTANTS ---
layers = 24
dram_bw_gbps = 50.0  
flash_bw_gbps = 3.0  
dram_energy_pj_per_byte = 45.0
flash_energy_pj_per_byte = 500.0  

# --- MODEL CONSTANTS (W4A4 Compressed Qwen1.5-MoE-A2.7B) ---
# FP16 payload was 1088MB full / 164MB active. W4A4 reduces this by 4x.
layer_full_mb = 272.0
layer_attn_shared_mb = 25.0
layer_active_experts_mb = 16.0   # 4 experts * 4MB
layer_active_total_mb = 41.0

# --- ARCHITECTURE ASSUMPTIONS ---
# 1GB RAM budget / 3.5MB per expert = 285 experts.
# 285 / 24 layers = 11 experts pinned PER LAYER (out of 60).
# Top 18.3% experts yield ~65% hit rate per layer.
dram_cache_hit_rate = 0.65   
lookahead_accuracy = 0.80    

def evaluate_architecture(name, dram_read_mb, flash_read_mb, flash_stall_mb, dram_write_mb=0):
    dram_time_ms = (dram_read_mb / 1024.0) / dram_bw_gbps * 1000
    flash_stall_time_ms = (flash_stall_mb / 1024.0) / flash_bw_gbps * 1000
    layer_time_ms = dram_time_ms + flash_stall_time_ms
    token_time_ms = layer_time_ms * layers
    tps = 1000.0 / token_time_ms if token_time_ms > 0 else 0
    
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

# 1. Baseline: Naive Flash Offload (W4A4 Full Layer)
res_naive = evaluate_architecture(
    "Baseline: Naive Flash Offload",
    dram_read_mb=layer_full_mb,
    flash_read_mb=layer_full_mb,
    flash_stall_mb=layer_full_mb,
    dram_write_mb=layer_full_mb
)
results.append(res_naive)

# 2. Pillar 3: Layer-wise Pinning + Streaming
p3_dram_read = layer_attn_shared_mb + (layer_active_experts_mb * dram_cache_hit_rate)
p3_flash_read = layer_active_experts_mb * (1.0 - dram_cache_hit_rate)
p3_flash_stall = p3_flash_read * (1.0 - lookahead_accuracy)
p3_dram_write = p3_flash_read

res_p3 = evaluate_architecture(
    "Proposed: Layer-wise Pillar 3",
    dram_read_mb=p3_dram_read + p3_flash_read,
    flash_read_mb=p3_flash_read,
    flash_stall_mb=p3_flash_stall,
    dram_write_mb=p3_dram_write
)
results.append(res_p3)

# 3. Upper Bound: Pure DRAM
res_dram = evaluate_architecture(
    "Upper Bound: Pure DRAM",
    dram_read_mb=layer_active_total_mb,
    flash_read_mb=0,
    flash_stall_mb=0,
    dram_write_mb=0
)
results.append(res_dram)

print(f"{'Architecture':<35} | {'Tokens/sec':>10} | {'mJ/Token':>10} | {'Latency/Tk':>10}")
print("-" * 75)
for r in results:
    print(f"{r['name']:<35} | {r['tps']:>10.2f} | {r['token_energy_mj']:>10.1f} | {r['token_time_ms']:>8.1f} ms")

