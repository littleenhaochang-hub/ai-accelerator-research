import time

def sim_sw_token_dropping_evaluation():
    # Simulate CPU/GPU software computing cosine similarity for dynamic depth token dropping
    time.sleep(0.52)
    return 520.0

def sim_hw_inline_cosine_similarity():
    # Simulate dedicated hardware comparator computing cosine similarity instantly
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_token_dropping_evaluation()
    hw = sim_hw_inline_cosine_similarity()
    print(f"Software Cosine Similarity Eval Latency: {sw:.2f} ms")
    print(f"Hardware Inline Cosine Similarity Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
