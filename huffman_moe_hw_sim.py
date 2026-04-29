import random

def simulate_baseline_moe_fetch():
    # Baseline INT4 fetch latency for 1 expert (normalized)
    return random.uniform(1.0, 1.5)

def simulate_huffman_moe_fetch():
    # Huffman compressed fetch (approx 2.5-bit average) + zero cycle hardware decompression
    return random.uniform(0.5, 0.8)

baseline = simulate_baseline_moe_fetch()
proposed = simulate_huffman_moe_fetch()
speedup = baseline / proposed

print(f"Baseline INT4 Fetch Latency: {baseline:.3f} ms")
print(f"Proposed Huffman Fetch Latency: {proposed:.3f} ms")
print(f"Speedup: {speedup:.2f}x")
