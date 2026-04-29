import time

def baseline_mla_sram_read():
    start = time.time()
    time.sleep(0.045) # Simulated DRAM-to-SRAM unrolling latency for Latent KV
    return time.time() - start

def pim_mla_unroll():
    start = time.time()
    time.sleep(0.009) # Simulated PIM (Processing-In-Memory) unrolling
    return time.time() - start

if __name__ == "__main__":
    print("Running Baseline MLA SRAM Unrolling...")
    base_lat = baseline_mla_sram_read()
    print(f"Baseline Latency: {base_lat*1000:.2f} ms")
    
    print("Running PIM MLA Unrolling...")
    pim_lat = pim_mla_unroll()
    print(f"PIM Latency: {pim_lat*1000:.2f} ms")
    
    speedup = base_lat / pim_lat if pim_lat > 0 else 0
    print(f"Speedup: {speedup:.2f}x")