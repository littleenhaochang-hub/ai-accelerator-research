import time

def simulate_hw_spsa():
    context_length = 65536
    
    # Baseline: Software FlashAttention computes dense Softmax over all chunks
    # then discards near-zero attention scores.
    # We estimate latency purely on the number of chunks processed.
    chunk_size = 256
    num_chunks = context_length // chunk_size
    baseline_chunk_latency = 1.5 # ms per chunk of dense attention
    baseline_latency_ms = num_chunks * baseline_chunk_latency
    
    # HW-SPSA: Hardware Sparsity Predictor & Skipper
    # Inline ultra-low precision predictor runs in 0.1ms per chunk.
    # It predicts 85% of chunks as irrelevant (bypassed).
    hw_predictor_latency = 0.1
    bypass_ratio = 0.85
    processed_chunks = num_chunks * (1 - bypass_ratio)
    
    # Total latency = predictor time (for all) + dense attention (for non-bypassed)
    hw_spsa_latency_ms = (num_chunks * hw_predictor_latency) + (processed_chunks * baseline_chunk_latency)
    
    print("=== HW-SPSA Simulation ===")
    print(f"Context Length: {context_length}")
    print(f"Baseline Latency (Dense FlashAttention): {baseline_latency_ms:.2f} ms")
    print(f"HW-SPSA Latency (Predict & Skip): {hw_spsa_latency_ms:.2f} ms")
    print(f"Speedup: {baseline_latency_ms/hw_spsa_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_spsa()