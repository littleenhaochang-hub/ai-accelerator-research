import time

def simulate_software_moe_routing(num_tokens, num_experts):
    # O(T * E) routing overhead in software
    latency = (num_tokens * num_experts) / 1e8
    return latency

def simulate_hw_dtrr_moe(num_tokens, num_experts):
    # O(1) hardware crossbar routing + bypassing idle experts
    latency = (num_tokens * 1) / 1e9 # Hardware switch latency
    return latency

if __name__ == "__main__":
    num_tokens = 4096
    num_experts = 256 # DeepSeek-style fine-grained experts
    
    soft_time = simulate_software_moe_routing(num_tokens, num_experts)
    hw_time = simulate_hw_dtrr_moe(num_tokens, num_experts)
    
    print(f"Software MoE Routing Latency: {soft_time:.4f} s")
    print(f"HW-DTRR MoE Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
