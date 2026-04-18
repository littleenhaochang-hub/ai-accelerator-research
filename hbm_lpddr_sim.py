import numpy as np

def simulate_hbm_vs_lpddr():
    print("Starting LPDDR vs HBM Energy & Bandwidth Hardware Simulation...")
    
    # 70B Model, W4A16 Quantization
    model_size_GB = 35.0
    
    # Simulate a generation of 1 token for a 70B model
    # To generate 1 token, the entire model must be read from DRAM once
    reads_GB = model_size_GB
    
    # --- System A: HBM3 (Cloud GPU typical) ---
    # Bandwidth: 3000 GB/s
    # Energy per bit: ~3.5 pJ/bit
    hbm_bandwidth = 3000
    hbm_latency_ms = (reads_GB / hbm_bandwidth) * 1000
    hbm_energy_joules = (reads_GB * 8 * 1e9) * (3.5 * 1e-12)
    
    # --- System B: LPDDR5X (Edge NPU typical, e.g., M-series Unified Memory) ---
    # Bandwidth: 400 GB/s (e.g. M3 Max)
    # Energy per bit: ~2.0 pJ/bit (LPDDR is optimized for mobile/edge)
    lpddr_bandwidth = 400
    lpddr_latency_ms = (reads_GB / lpddr_bandwidth) * 1000
    lpddr_energy_joules = (reads_GB * 8 * 1e9) * (2.0 * 1e-12)
    
    print(f"Model Workload: {model_size_GB} GB per token")
    print("\n[HBM3 Cloud GPU]")
    print(f"Latency per token: {hbm_latency_ms:.2f} ms ({1000/hbm_latency_ms:.1f} tok/s)")
    print(f"DRAM Energy per token: {hbm_energy_joules:.2f} Joules")
    
    print("\n[LPDDR5X Edge NPU]")
    print(f"Latency per token: {lpddr_latency_ms:.2f} ms ({1000/lpddr_latency_ms:.1f} tok/s)")
    print(f"DRAM Energy per token: {lpddr_energy_joules:.2f} Joules")
    
    print(f"\nEnergy Savings (LPDDR vs HBM): {(1 - lpddr_energy_joules/hbm_energy_joules)*100:.2f}%")
    print(f"Bandwidth Gap: LPDDR is {hbm_bandwidth/lpddr_bandwidth:.1f}x slower.")
    
    print("\nConclusion: LPDDR5X is significantly more energy-efficient but lacks the bandwidth for high-TPS 70B model inference. Hardware requires pushing more compute on-chip (SRAM/CIM) and using extreme weight quantization (sub-3-bit) to bridge the 7.5x bandwidth gap while keeping the energy benefits of LPDDR.")

if __name__ == "__main__":
    simulate_hbm_vs_lpddr()