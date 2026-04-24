import time

def draft_model_spec_decoding(tokens):
    # Simulated latency using a small 1B draft model (memory + compute)
    draft_lat = tokens * 0.015
    return draft_lat

def ngram_sram_spec_decoding(tokens):
    # Simulated latency using a hardware SRAM N-gram cache lookup
    ngram_lat = tokens * 0.001
    return ngram_lat

def main():
    tokens = 2048
    print("Running Hardware N-Gram Speculative Decoding Simulation...")
    draft_lat = draft_model_spec_decoding(tokens)
    print(f"Draft Model Speculative Latency: {draft_lat:.2f} ms")
    
    ngram_lat = ngram_sram_spec_decoding(tokens)
    print(f"SRAM N-Gram Speculative Latency: {ngram_lat:.2f} ms")
    
    speedup = draft_lat / ngram_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
