import time

def simulate_standard_backprop(num_layers, seq_len, dim):
    print(f"Simulating Standard Backpropagation (Layers={num_layers})...")
    start = time.time()
    # High memory bandwidth for reading saved activations
    time.sleep(0.6)
    latency = time.time() - start
    memory_mb = (num_layers * seq_len * dim * 2) / (1024**2) # FP16
    return latency, memory_mb

def simulate_reversible_backprop(num_layers, seq_len, dim):
    print(f"Simulating Hardware Reversible Backpropagation...")
    start = time.time()
    # Recomputing activations on-the-fly saves memory but adds slight compute latency
    # Hardware ALUs optimized for inverse operations mask most of this
    time.sleep(0.75) 
    latency = time.time() - start
    memory_mb = (1 * seq_len * dim * 2) / (1024**2) # Only last layer saved
    return latency, memory_mb

num_layers = 32
seq_len = 8192
dim = 4096

std_lat, std_mem = simulate_standard_backprop(num_layers, seq_len, dim)
rev_lat, rev_mem = simulate_reversible_backprop(num_layers, seq_len, dim)

print(f"\nResults:")
print(f"Standard Training Latency: {std_lat:.4f} s | Activation Memory: {std_mem:.2f} MB")
print(f"Reversible Training Latency: {rev_lat:.4f} s | Activation Memory: {rev_mem:.2f} MB")
print(f"Memory Reduction: {std_mem/rev_mem:.2f}x")
