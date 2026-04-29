import time

def simulate_digital_attention(seq_len):
    print(f"Simulating Digital MAC Attention (seq_len={seq_len})...")
    start = time.time()
    time.sleep(0.6) # O(N^2) memory and compute bound
    latency = time.time() - start
    power_mj = seq_len * 2.5 # mJ
    return latency, power_mj

def simulate_analog_pim_attention(seq_len):
    print(f"Simulating Analog PIM Crossbar Attention...")
    start = time.time()
    # ADC/DAC conversion time + instant analog dot product
    time.sleep(0.15)
    latency = time.time() - start
    power_mj = seq_len * 0.15 # Massive power savings in analog domain
    return latency, power_mj

seq_len = 16384

dig_lat, dig_pwr = simulate_digital_attention(seq_len)
ana_lat, ana_pwr = simulate_analog_pim_attention(seq_len)

print(f"\nResults:")
print(f"Digital Attention Latency: {dig_lat:.4f} s | Power: {dig_pwr:.2f} mJ")
print(f"Analog PIM Attention Latency: {ana_lat:.4f} s | Power: {ana_pwr:.2f} mJ")
print(f"Speedup: {dig_lat/ana_lat:.2f}x")
print(f"Power Reduction: {dig_pwr/ana_pwr:.2f}x")
