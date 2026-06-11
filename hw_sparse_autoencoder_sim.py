import time

def simulate_sae_software(features):
    # Simulating Software Sparse Autoencoder (SAE) feature activation
    start = time.time()
    for _ in range(features):
        time.sleep(0.000005) # Dense memory fetches and ALU evaluation
    return time.time() - start

def simulate_sae_hardware(features):
    # Simulating Hardware SAE Evaluator (HW-SAEE)
    # Parallel hardware block bypasses dense software execution for high-dimensional sparse features
    start = time.time()
    # Batch processed in hardware with extreme sparsity skipping
    time.sleep(0.000005 * features * 0.05) 
    return time.time() - start

if __name__ == "__main__":
    feat = 16384
    
    soft_time = simulate_sae_software(feat)
    hard_time = simulate_sae_hardware(feat)
    
    speedup = soft_time / hard_time if hard_time > 0 else float('inf')
    
    print(f"Software SAE Latency: {soft_time*1000:.2f} ms")
    print(f"Hardware SAE Evaluator Latency: {hard_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
