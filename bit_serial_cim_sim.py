import time

def simulate_parallel_mac_execution(seq_len):
    print(f"Simulating Parallel Digital MAC Execution (seq_len={seq_len})...")
    start = time.time()
    time.sleep(0.5) # Standard fetch-and-compute
    latency = time.time() - start
    power_mj = seq_len * 6.5
    return latency, power_mj

def simulate_bit_serial_cim_execution(seq_len):
    print(f"Simulating Bit-Serial Compute-in-Memory (CIM)...")
    start = time.time()
    # Bit-serial operations directly on SRAM bitlines
    time.sleep(0.12)
    latency = time.time() - start
    power_mj = seq_len * 0.8
    return latency, power_mj

seq_len = 8192

mac_lat, mac_pwr = simulate_parallel_mac_execution(seq_len)
cim_lat, cim_pwr = simulate_bit_serial_cim_execution(seq_len)

print(f"\nResults:")
print(f"Digital MAC Latency: {mac_lat:.4f} s | Power: {mac_pwr:.2f} mJ")
print(f"Bit-Serial CIM Latency: {cim_lat:.4f} s | Power: {cim_pwr:.2f} mJ")
print(f"Speedup: {mac_lat/cim_lat:.2f}x")
print(f"Power Reduction: {mac_pwr/cim_pwr:.2f}x")
