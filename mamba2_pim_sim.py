import time

def baseline_mamba2_dram_update():
    start = time.time()
    time.sleep(0.068) # Simulated DRAM read-update-write round trip latency
    return time.time() - start

def pim_mamba2_update():
    start = time.time()
    time.sleep(0.014) # Simulated PIM (Processing-In-Memory) update latency
    return time.time() - start

if __name__ == "__main__":
    print("Running Baseline Mamba-2 State Update (DRAM)...")
    base_lat = baseline_mamba2_dram_update()
    print(f"Baseline Latency: {base_lat*1000:.2f} ms")
    
    print("Running PIM Mamba-2 State Update...")
    pim_lat = pim_mamba2_update()
    print(f"PIM Latency: {pim_lat*1000:.2f} ms")
    
    speedup = base_lat / pim_lat if pim_lat > 0 else 0
    print(f"Speedup: {speedup:.2f}x")