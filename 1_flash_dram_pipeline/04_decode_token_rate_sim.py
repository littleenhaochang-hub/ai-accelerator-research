import math

print("=== Decode Token Rate Simulation (24-Layer MoE Model) ===")
layers = 24
flash_bw_gbps = 3.0  # UFS 4.0
dram_bw_gbps = 50.0  # LPDDR5x

# Payloads per layer (from previous script)
full_layer_mb = 1088.0
dynamic_layer_mb = 164.0

def calc_rate(name, time_per_layer_ms):
    total_ms = time_per_layer_ms * layers
    tps = 1000.0 / total_ms if total_ms > 0 else 0
    print(f"| {name:<40} | {time_per_layer_ms:>10.2f} ms | {total_ms:>12.2f} ms | {tps:>15.2f} T/s |")

print(f"| {'Architecture Strategy':<40} | {'Layer Time':>13} | {'Token Latency':>15} | {'Decode Rate':>19} |")
print("|" + "-"*42 + "|" + "-"*14 + "|" + "-"*17 + "|" + "-"*21 + "|")

# 1. Naive Flash Offload (Read 1088 MB from Flash)
time_naive_ms = (full_layer_mb / 1024.0) / flash_bw_gbps * 1000
calc_rate("1. Naive Flash Offload (Full Layer)", time_naive_ms)

# 2. Dynamic Streaming (Read 164 MB from Flash)
time_dynamic_ms = (dynamic_layer_mb / 1024.0) / flash_bw_gbps * 1000
calc_rate("2. Dynamic Streaming (Pure Flash)", time_dynamic_ms)

# 3. Dynamic Streaming + Pinning + Lookahead
# Let's say Attention+Shared (100MB) is pinned in DRAM. 
# Active experts (64MB) are 80% cached in DRAM, 20% fetched from Flash (with 80% lookahead hidden).
# Effective Flash read per layer = 64MB * 0.20 miss rate * 0.20 stall rate = 2.56 MB from Flash
# DRAM read per layer = 100MB + 64MB = 164 MB from DRAM
time_flash_stall_ms = (2.56 / 1024.0) / flash_bw_gbps * 1000
time_dram_read_ms = (164.0 / 1024.0) / dram_bw_gbps * 1000
time_pillar3_ms = time_flash_stall_ms + time_dram_read_ms
calc_rate("3. Pillar 3 (Streaming + Pin + Prefetch)", time_pillar3_ms)

# 4. Pure DRAM (Upper Bound, assuming infinite RAM)
time_dram_ms = (dynamic_layer_mb / 1024.0) / dram_bw_gbps * 1000
calc_rate("4. Pure DRAM (Theoretical Upper Bound)", time_dram_ms)

