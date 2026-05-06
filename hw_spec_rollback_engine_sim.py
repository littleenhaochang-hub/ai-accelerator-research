import time
import numpy as np

def simulate_software_speculative_rollback(num_tokens=64, layers=32):
    # Software: On miss, software must manually clear KV cache pointers, reset SM states, and re-fetch correct branch
    print(f"Simulating Software Speculative Rollback (Missed Tokens: {num_tokens})...")
    latency = num_tokens * layers * 0.00001 # Software state management overhead
    return latency

def simulate_hardware_spec_rollback_engine(num_tokens=64, layers=32):
    # HW-SERE: Hardware maintains a shadow pointer table for the KV cache and instantly reverts on miss
    print(f"Simulating Hardware Speculative Execution Rollback Engine (HW-SERE)...")
    latency = layers * 0.0000001 # O(1) per layer pointer swap
    return latency

if __name__ == "__main__":
    sw_lat = simulate_software_speculative_rollback()
    hw_lat = simulate_hardware_spec_rollback_engine()
    
    print(f"Software Rollback Latency: {sw_lat:.5f} s")
    print(f"HW-SERE Latency: {hw_lat:.5f} s")
    print(f"Latency Speedup: {sw_lat/hw_lat:.2f}x")
