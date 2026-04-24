import time

def software_expert_pruning(tokens, num_experts, prune_ratio):
    # Simulated latency for software dynamic expert pruning
    # Evaluates router logits, zeros out bottom E*prune_ratio experts dynamically
    # Software overhead to mask and re-normalize
    latency = tokens * num_experts * 0.005 # ms
    return latency

def hardware_expert_pruner(tokens, num_experts, prune_ratio):
    # Simulated latency for an inline Hardware MoE Expert Pruner
    # Router ALU directly zeros out logits below a threshold before Top-K selection
    latency = tokens * num_experts * 0.0003 # ms
    return latency

def main():
    tokens = 4096
    num_experts = 128
    prune_ratio = 0.5 # Drop the bottom 50% of experts entirely from memory fetching considerations
    
    print("Running Hardware MoE Expert Pruning Simulation...")
    sw_lat = software_expert_pruning(tokens, num_experts, prune_ratio)
    print(f"Software Expert Pruning Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_expert_pruner(tokens, num_experts, prune_ratio)
    print(f"Hardware Expert Pruning Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
