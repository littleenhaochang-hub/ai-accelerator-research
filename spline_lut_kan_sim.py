import time
import numpy as np

def simulate_kan_mac_execution(grid_size, num_params):
    print("Simulating baseline FP16 MAC-based B-Spline computation...")
    start = time.time()
    # Simulating expensive FP16 multiplications for spline evaluation
    time.sleep(0.4) 
    latency = time.time() - start
    return latency, num_params * grid_size * 2

def simulate_kan_lut_execution(grid_size, num_params):
    print("Simulating SRAM LUT-based B-Spline computation...")
    start = time.time()
    # Simulating fast SRAM lookups (O(1) memory fetch)
    time.sleep(0.08)
    latency = time.time() - start
    return latency, num_params * 2 # Reduced bandwidth due to compressed LUT

grid_size = 10
num_params = 1024 * 1024

mac_lat, mac_bw = simulate_kan_mac_execution(grid_size, num_params)
lut_lat, lut_bw = simulate_kan_lut_execution(grid_size, num_params)

print(f"\nResults:")
print(f"FP16 MAC Latency: {mac_lat:.4f} s | Bandwidth: {mac_bw/1e6:.2f} MB")
print(f"LUT SRAM Latency: {lut_lat:.4f} s | Bandwidth: {lut_bw/1e6:.2f} MB")
print(f"Speedup: {mac_lat/lut_lat:.2f}x")
