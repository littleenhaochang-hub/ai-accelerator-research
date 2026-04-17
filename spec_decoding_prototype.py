import math
import random

def simulate_speculative_decoding_hardware():
    print("Initializing Speculative Decoding Hardware Co-Design Simulation...")
    
    # Simulating token generation times (in milliseconds)
    target_model_time = 15.0  # Big LLM generation time per token
    draft_model_time = 2.0    # Small draft model generation time per token
    target_verify_time = 16.0 # Big LLM verification time for a batch of draft tokens
    
    # Simulation settings
    total_tokens_needed = 100
    gamma = 4  # Number of tokens to draft per step
    acceptance_rate = 0.7  # 70% probability a draft token is accepted
    
    # 1. Baseline Auto-regressive Latency
    baseline_latency = total_tokens_needed * target_model_time
    
    # 2. Speculative Decoding Latency
    tokens_generated = 0
    speculative_latency = 0.0
    steps = 0
    
    while tokens_generated < total_tokens_needed:
        # Step 1: Draft model generates gamma tokens
        draft_time_cost = gamma * draft_model_time
        speculative_latency += draft_time_cost
        
        # Step 2: Target model verifies all draft tokens in parallel
        speculative_latency += target_verify_time
        
        # Step 3: Determine how many were accepted
        accepted_count = 0
        for _ in range(gamma):
            if random.random() < acceptance_rate:
                accepted_count += 1
            else:
                break # Stop at first rejection
                
        # The target model always generates 1 guaranteed token during verification
        tokens_generated += accepted_count + 1
        steps += 1
        
    print(f"Total tokens requested: {total_tokens_needed}")
    print(f"Baseline Auto-regressive Latency: {baseline_latency:.2f} ms")
    print(f"Speculative Decoding Latency: {speculative_latency:.2f} ms (in {steps} steps)")
    speedup = baseline_latency / speculative_latency
    print(f"Speedup: {speedup:.2f}x")
    
    print("\nHardware Accelerator Need: Reconfigurable PE arrays for parallel draft/verify passes.")
    print("FSD-Acc (Fused Speculative Decoding) concept: Weight sharing and unified GEMMs to prevent PCIe bottlenecks between Draft and Target NPUs.")

if __name__ == "__main__":
    simulate_speculative_decoding_hardware()