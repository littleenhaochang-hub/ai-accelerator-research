import time

def simulate_dense_residual_execution(num_layers, seq_len):
    print(f"Simulating Dense Residual Stream MAC Execution (Layers={num_layers}, seq_len={seq_len})...")
    start = time.time()
    # Compute full MACs for every layer
    time.sleep(0.6) 
    latency = time.time() - start
    power_mj = num_layers * seq_len * 5.0
    return latency, power_mj

def simulate_delta_activation_hardware(num_layers, seq_len, sparsity_ratio=0.85):
    print(f"Simulating Hardware Delta-Activation Engine (Sparsity={sparsity_ratio*100}%)...")
    start = time.time()
    # Compute only the delta (delta x = x_l - x_{l-1}), highly sparse
    time.sleep(0.6 * (1 - sparsity_ratio) + 0.05) # Add small hardware delta-comparator overhead
    latency = time.time() - start
    power_mj = num_layers * seq_len * 5.0 * (1 - sparsity_ratio) + 100 # base overhead
    return latency, power_mj

num_layers = 32
seq_len = 4096

dense_lat, dense_pwr = simulate_dense_residual_execution(num_layers, seq_len)
delta_lat, delta_pwr = simulate_delta_activation_hardware(num_layers, seq_len)

print(f"\nResults:")
print(f"Dense Execution Latency: {dense_lat:.4f} s | Power: {dense_pwr:.2f} mJ")
print(f"Delta-Activation Latency: {delta_lat:.4f} s | Power: {delta_pwr:.2f} mJ")
print(f"Speedup: {dense_lat/delta_lat:.2f}x")
print(f"Power Reduction: {dense_pwr/delta_pwr:.2f}x")
