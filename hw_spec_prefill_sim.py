import time

def simulate_hw_spec_prefill():
    num_tokens = 8192
    
    # Baseline: standard prefill
    baseline_latency_ms = num_tokens * 0.05 # 50us per token
    
    # Proposed: HW-Speculative-Prefill
    # Guessing chunk outputs with a tiny hardware predictor, only verifying
    draft_latency_ms = num_tokens * 0.005 # 5us per token draft
    verification_latency_ms = num_tokens * 0.015 # 15us per token verify
    
    proposed_latency_ms = draft_latency_ms + verification_latency_ms
    
    print("=== HW-Speculative-Prefill Simulation ===")
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-Speculative Latency: {proposed_latency_ms:.2f} ms")
    print(f"Speedup: {baseline_latency_ms/proposed_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_spec_prefill()
