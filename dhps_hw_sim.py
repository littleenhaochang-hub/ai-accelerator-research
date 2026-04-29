import time

def simulate_static_precision(seq_len):
    print(f"Simulating Static INT4 Execution (seq_len={seq_len})...")
    start = time.time()
    time.sleep(0.4) 
    latency = time.time() - start
    bandwidth_bits = seq_len * 4 
    return latency, bandwidth_bits

def simulate_dynamic_precision(seq_len):
    print(f"Simulating Dynamic Hardware Precision Scaling (DHPS)...")
    start = time.time()
    # 10% INT8 (high attention), 30% INT4 (medium), 60% INT2 (background)
    time.sleep(0.4 * 0.1 + 0.2 * 0.3 + 0.1 * 0.6 + 0.02) # included hardware router overhead
    latency = time.time() - start
    bandwidth_bits = seq_len * (8 * 0.1 + 4 * 0.3 + 2 * 0.6)
    return latency, bandwidth_bits

seq_len = 8192

static_lat, static_bw = simulate_static_precision(seq_len)
dyn_lat, dyn_bw = simulate_dynamic_precision(seq_len)

print(f"\nResults:")
print(f"Static INT4 Latency: {static_lat:.4f} s | Avg Bits/Token: 4.0")
print(f"DHPS Latency: {dyn_lat:.4f} s | Avg Bits/Token: {dyn_bw/seq_len:.2f}")
print(f"Speedup: {static_lat/dyn_lat:.2f}x")
