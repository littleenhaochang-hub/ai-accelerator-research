import numpy as np

def simulate_hw_spec_draft_validator(draft_len, vocab_size):
    print(f"Simulating Hardware Speculative Draft Validator (HW-SDV) - Draft Length: {draft_len}")
    
    # Software Verification (CPU bound)
    # CPU reads target logits, runs softmax, samples, and compares arrays
    sw_latency = (vocab_size * draft_len) / (50e9) * 1000 + 0.1 # Memory bound + CPU overhead
    
    # HW-SDV: Dedicated inline comparator array inside the NPU
    # Target logits directly stream through the comparator array matching against cached draft tokens
    # Bypasses softmax entirely for exact matches (greedy decoding path)
    hw_latency = (draft_len * 4) / (800e9) * 1000 + 0.005 # Register level comparison
    
    print(f"Software Verification Latency: {sw_latency:.4f} ms")
    print(f"HW-SDV Latency: {hw_latency:.4f} ms")
    print(f"Latency Reduction: {(sw_latency - hw_latency) / sw_latency * 100:.2f}%")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_spec_draft_validator(64, 128256)
