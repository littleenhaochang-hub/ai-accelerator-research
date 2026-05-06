import time

def simulate_hw_adee():
    num_tokens = 8192
    hidden_dim = 4096
    
    # Baseline: Full dense activation SRAM write/read
    # FP16 = 2 bytes
    activation_size_mb = (num_tokens * hidden_dim * 2) / (1024 * 1024)
    sram_bw_gbps = 2000
    baseline_latency_ms = (activation_size_mb / 1024) / sram_bw_gbps * 1000 * 2.0 # write and read
    
    # HW-ADEE (Hardware Activation Delta-Encoding Engine)
    # Exploit token-to-token similarity. Send only significant deltas.
    # Assume 75% of activation values have negligible change (delta < threshold)
    sparsity_ratio = 0.75
    # Overhead for bitmask
    bitmask_size_mb = (num_tokens * hidden_dim) / 8 / (1024 * 1024)
    
    encoded_activation_size_mb = activation_size_mb * (1 - sparsity_ratio) + bitmask_size_mb
    
    fuser_latency_ms = (encoded_activation_size_mb / 1024) / sram_bw_gbps * 1000 * 2.0
    
    print("=== HW-ADEE Simulation ===")
    print(f"Sequence Length: {num_tokens}")
    print(f"Baseline SRAM Traffic: {activation_size_mb*2:.2f} MB")
    print(f"HW-ADEE SRAM Traffic: {encoded_activation_size_mb*2:.2f} MB")
    print(f"Baseline Latency: {baseline_latency_ms:.4f} ms")
    print(f"HW-ADEE Latency: {fuser_latency_ms:.4f} ms")
    print(f"Speedup: {baseline_latency_ms/fuser_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_adee()
