import json
import os

print("=== Gemma-4 26B Data Flow & Pipeline Simulator ===")
print("Modeling system initialization, Early-Routing, and UFS 4.0 Flash Layout constraints.")

# Hardware Constants
FLASH_BW_GBPS = 3.0       # UFS 4.0 Sequential Read
FLASH_LATENCY_MS = 0.5    # UFS Random Read Setup Latency (ms)
DRAM_BW_GBPS = 50.0       # LPDDR5x
DRAM_ENERGY_PJ_BYTE = 45.0
FLASH_ENERGY_PJ_BYTE = 500.0

# Model Constraints (5GB Budget Scenario)
PINNED_BASE_GB = 1.2
HOT_EXPERTS_PER_LAYER = 42
EXPERT_SIZE_MB = 3.04
LAYERS = 30
ACTIVE_EXPERTS = 8
HIT_RATE = 0.873

def simulate_data_flow():
    # 1. System Initialization (Cold Boot)
    hot_experts_gb = (HOT_EXPERTS_PER_LAYER * EXPERT_SIZE_MB * LAYERS) / 1024.0
    total_dram_load_gb = PINNED_BASE_GB + hot_experts_gb
    init_time_sec = total_dram_load_gb / FLASH_BW_GBPS
    
    print(f"\n[Phase 1: Cold Boot Initialization]")
    print(f"Loading Base Weights (1.2GB) + Offline Hot Experts ({hot_experts_gb:.2f}GB) into LPDDR5x.")
    print(f"Total Boot Read: {total_dram_load_gb:.2f} GB")
    print(f"Init Latency (UFS 4.0 -> DDR): {init_time_sec:.2f} seconds")

    # 2. Runtime Dynamic Inference (Per Token)
    # Per layer breakdown
    experts_hit = ACTIVE_EXPERTS * HIT_RATE
    experts_miss = ACTIVE_EXPERTS * (1.0 - HIT_RATE)
    
    # Dram Transfer Time (Hits + Misses eventually go to DRAM/SRAM)
    dram_payload_mb = ACTIVE_EXPERTS * EXPERT_SIZE_MB
    dram_time_ms = dram_payload_mb / DRAM_BW_GBPS
    
    # Flash Transfer Time (Misses)
    flash_payload_mb = experts_miss * EXPERT_SIZE_MB
    flash_transfer_time_ms = flash_payload_mb / FLASH_BW_GBPS
    # Add random read latency penalty per missed expert block
    flash_total_time_ms = (experts_miss * FLASH_LATENCY_MS) + flash_transfer_time_ms
    
    # Early-Router Overlap: If we calculate router 1 layer ahead, we can hide some flash time
    compute_time_ms = 1.5 # assumed MAC compute time per layer
    hidden_flash_time = min(flash_total_time_ms, compute_time_ms)
    stall_time_ms = flash_total_time_ms - hidden_flash_time if flash_total_time_ms > hidden_flash_time else 0
    
    layer_latency_ms = dram_time_ms + stall_time_ms + compute_time_ms
    total_token_latency_ms = layer_latency_ms * LAYERS
    tps = 1000.0 / total_token_latency_ms

    print(f"\n[Phase 2: Runtime Pipeline (Per Layer)]")
    print(f"Target Experts: 8. Hit (DRAM): {experts_hit:.2f}. Miss (Flash): {experts_miss:.2f}")
    print(f"Flash Raw Fetch Time: {flash_total_time_ms:.3f} ms")
    print(f"Early-Router Hidden Time: {hidden_flash_time:.3f} ms")
    print(f"Pipeline Stall Time: {stall_time_ms:.3f} ms")
    
    print(f"\n[Phase 3: UFS 4.0 Layout Impact]")
    print("Optimization: If cold experts are scattered, LBA fragmentation increases FLASH_LATENCY.")
    print("By enforcing 4KB page-aligned contiguous layout for cold experts, we limit penalty to 0.5ms.")

    print(f"\n[Final Metrics]")
    print(f"Speed: {tps:.2f} Tokens/sec")
    print(f"Time per Token: {total_token_latency_ms:.2f} ms")

if __name__ == "__main__":
    simulate_data_flow()
