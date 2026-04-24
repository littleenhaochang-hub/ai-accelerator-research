import time
import numpy as np

def sim_standard_autoregressive(tokens, d_model, vocab_size):
    # Standard AR decoding: Fetch KV, Compute Attention, Compute FFN, Compute Logits
    macs_per_token = 2 * d_model * vocab_size # simplified projection
    latency = 0.0
    for _ in range(tokens):
        # Memory fetch latency + compute latency
        latency += 0.05 + (macs_per_token / 1e12) * 0.01 
    return latency

def sim_mtp_hardware(tokens, k_depth, d_model, vocab_size):
    # Multi-Token Prediction (MTP): predict K tokens at once using shared state + fast projection
    # Hardware feature: parallel MTP heads on-chip
    macs_per_head = 2 * d_model * vocab_size
    latency = 0.0
    
    # Assuming acceptance rate of roughly 2.5 tokens per MTP pass
    effective_steps = tokens / 2.5
    for _ in range(int(effective_steps)):
        # One pass predicts K tokens. Memory fetch latency happens ONCE for base state.
        # Compute happens in parallel across K heads.
        latency += 0.06 + (macs_per_head / 1e12) * 0.01
    return latency

def main():
    tokens = 1000
    d_model = 4096
    vocab_size = 32000
    k_depth = 4 # Predict 4 tokens into the future

    print("Running Standard Autoregressive Decoding Simulation...")
    ar_lat = sim_standard_autoregressive(tokens, d_model, vocab_size)
    print(f"Standard AR Latency: {ar_lat:.4f} s")

    print(f"Running MTP (Multi-Token Prediction K={k_depth}) Hardware Simulation...")
    mtp_lat = sim_mtp_hardware(tokens, k_depth, d_model, vocab_size)
    print(f"MTP Latency: {mtp_lat:.4f} s")

    speedup = ar_lat / mtp_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
