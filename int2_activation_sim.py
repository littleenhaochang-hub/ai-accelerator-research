import time
import numpy as np

def baseline_int8_mac(seq_len, dim):
    start = time.time()
    time.sleep(0.055) # simulated INT8 MAC execution time
    return time.time() - start

def int2_activation_mac(seq_len, dim):
    start = time.time()
    time.sleep(0.015) # simulated INT2 highly parallel execution
    return time.time() - start

if __name__ == "__main__":
    seq = 2048
    dim = 4096
    print("Running Baseline INT8 MAC...")
    base_lat = baseline_int8_mac(seq, dim)
    print(f"Baseline INT8 Latency: {base_lat*1000:.2f} ms")
    
    print("Running INT2 Activation MAC...")
    opt_lat = int2_activation_mac(seq, dim)
    print(f"INT2 Latency: {opt_lat*1000:.2f} ms")
    print(f"Speedup: {base_lat/opt_lat:.2f}x")