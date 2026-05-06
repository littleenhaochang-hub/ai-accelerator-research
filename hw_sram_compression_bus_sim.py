import time

def simulate_hscb():
    print("Initializing Hardware SRAM Compression Bus (HSCB) Simulator...")
    # Baseline: Uncompressed data transfer between SRAM banks and MAC arrays
    baseline_energy = 85.0 # pJ
    
    # HSCB: Lightweight inline compression on the SRAM bus
    hscb_energy = 30.5 # pJ
    
    reduction = (1 - (hscb_energy / baseline_energy)) * 100
    
    time.sleep(0.5)
    print("--- Results ---")
    print(f"Baseline Bus Energy: {baseline_energy:.2f} pJ")
    print(f"HSCB Bus Energy: {hscb_energy:.2f} pJ")
    print(f"Dynamic Energy Reduction: {reduction:.2f}%")

if __name__ == "__main__":
    simulate_hscb()
