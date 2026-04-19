def simulate_draft_coprocessor():
    print("=== Speculative Decoding: Draft Co-Processor Simulation ===")
    
    # Latencies in ms
    main_npu_latency_per_token = 20.0
    cpu_draft_latency = 15.0
    coprocessor_draft_latency = 2.0
    
    # Average accepted tokens per step
    gamma = 3.0
    
    # Base TPS without speculative decoding
    base_tps = 1000.0 / main_npu_latency_per_token
    
    # TPS with CPU generating draft tokens
    cpu_spec_tps = (gamma + 1) * 1000.0 / (cpu_draft_latency * gamma + main_npu_latency_per_token)
    
    # TPS with dedicated Draft Co-Processor
    coprocessor_spec_tps = (gamma + 1) * 1000.0 / (coprocessor_draft_latency * gamma + main_npu_latency_per_token)
    
    speedup = coprocessor_spec_tps / base_tps
    
    print(f"Base TPS: {base_tps:.2f}")
    print(f"CPU-Draft Speculative TPS: {cpu_spec_tps:.2f}")
    print(f"Co-Processor Speculative TPS: {coprocessor_spec_tps:.2f}")
    print(f"Speedup vs Base: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_draft_coprocessor()
