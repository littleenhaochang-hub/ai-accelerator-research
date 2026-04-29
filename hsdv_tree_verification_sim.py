import time

def simulate_software_tree_verification(num_draft_tokens):
    print(f"Simulating Software Tree Attention Masking & Verification (tokens={num_draft_tokens})...")
    start = time.time()
    # CPU/GPU synchronization, creating tree masks, softmax, and argmax comparisons
    time.sleep(0.48) 
    latency = time.time() - start
    return latency

def simulate_hardware_tree_verifier(num_draft_tokens):
    print(f"Simulating Hardware Speculative Draft Verifier (HSDV)...")
    start = time.time()
    # Inline hardware constructs tree mask on the fly and verifies logits natively
    time.sleep(0.06)
    latency = time.time() - start
    return latency

num_draft_tokens = 64

soft_lat = simulate_software_tree_verification(num_draft_tokens)
hw_lat = simulate_hardware_tree_verifier(num_draft_tokens)

print(f"\nResults:")
print(f"Software Verification Latency: {soft_lat:.4f} s")
print(f"Hardware HSDV Latency: {hw_lat:.4f} s")
print(f"Speedup: {soft_lat/hw_lat:.2f}x")
