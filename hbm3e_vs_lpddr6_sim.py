import time

def simulate_hbm3e_vs_lpddr6():
    print("Simulating HBM3e vs LPDDR6 for Ultra-Edge LLM Inference (Re-evaluation)...")
    
    # 7B dense model INT4 -> ~3.5 GB memory needed
    # Memory Bandwidth
    lpddr6_bw_gbs = 120 # Overclocked LPDDR6
    hbm3e_bw_gbs = 1200 # Single stack HBM3e
    
    # Energy per bit (pJ/bit)
    lpddr6_energy_pj_per_bit = 3.5
    hbm3e_energy_pj_per_bit = 3.0
    
    # Area / Packaging cost
    lpddr6_packaging_cost = 1.0 
    hbm3e_packaging_cost = 15.0  # CoWoS-S
    
    # TPS Calculation (Memory bound decoding)
    lpddr6_tps = lpddr6_bw_gbs / 3.5
    hbm3e_tps = hbm3e_bw_gbs / 3.5
    
    # Power for reading weights continuously at max TPS
    lpddr6_power_w = (lpddr6_bw_gbs * 8 * 1e9 * lpddr6_energy_pj_per_bit * 1e-12)
    hbm3e_power_w = (hbm3e_bw_gbs * 8 * 1e9 * hbm3e_energy_pj_per_bit * 1e-12)
    
    print(f"LPDDR6 TPS: {lpddr6_tps:.2f} | Power: {lpddr6_power_w:.2f}W | Cost: {lpddr6_packaging_cost}x")
    print(f"HBM3e TPS:  {hbm3e_tps:.2f} | Power: {hbm3e_power_w:.2f}W | Cost: {hbm3e_packaging_cost}x")
    
    print("\nConclusion: Re-confirmed. HBM3e draws nearly 30W purely for memory I/O at max throughput. LPDDR6 at 3.36W is the hard ceiling for portable/passive Edge NPUs.")

if __name__ == '__main__':
    simulate_hbm3e_vs_lpddr6()
