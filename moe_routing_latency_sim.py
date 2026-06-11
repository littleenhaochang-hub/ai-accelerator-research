import time

def simulate_traditional_moe_routing(num_tokens, num_experts):
    # Simulates software mediation phase: address resolution before data transfer
    start = time.time()
    for _ in range(num_tokens):
        # Software abstraction mismatch overhead
        time.sleep(0.00005) 
    return time.time() - start

def simulate_moe_hub_routing(num_tokens, num_experts):
    # Simulates MoE-Hub destination-agnostic communication paradigm
    # Hardware handles address allocation, pipelined with routing
    start = time.time()
    for _ in range(num_tokens):
        # HW-accelerated control plane
        time.sleep(0.000001)
    return time.time() - start

if __name__ == "__main__":
    tokens = 32768
    experts = 64
    
    trad_time = simulate_traditional_moe_routing(tokens, experts)
    hub_time = simulate_moe_hub_routing(tokens, experts)
    
    speedup = trad_time / hub_time if hub_time > 0 else float('inf')
    
    print(f"Traditional MoE Routing Latency: {trad_time*1000:.2f} ms")
    print(f"HW-MoE-Hub Routing Latency: {hub_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
