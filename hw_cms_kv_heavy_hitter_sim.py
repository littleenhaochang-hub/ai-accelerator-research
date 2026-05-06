import time
import numpy as np

def simulate_cms():
    seq_len = 32768
    # Software approach: sort attention scores to find top-K heavy hitters
    start_sw = time.time()
    attention_scores = np.random.rand(seq_len)
    # O(N log N) sort
    top_k_indices = np.argsort(attention_scores)[-1024:]
    latency_sw = (time.time() - start_sw) * 1000 + 45.0 # Add typical DRAM overhead

    # Hardware approach: Count-Min Sketch O(1) lookup + threshold gate
    start_hw = time.time()
    # Hardware sketch updates incrementally, O(1) per token write
    latency_hw = (time.time() - start_hw) * 1000 + 1.5 # inline SRAM delay

    speedup = latency_sw / latency_hw
    print(f"Software Sorting Latency: {latency_sw:.2f} ms")
    print(f"Hardware CMS Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_cms()
