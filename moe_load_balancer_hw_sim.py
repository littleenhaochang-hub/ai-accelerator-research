import time
import random

def software_moe_load_balancing(tokens, num_experts):
    # Simulated latency for software-based expert load balancing (e.g., adding noise, capacity limits)
    # Requires scanning tokens, tracking capacity, and re-routing overflows
    compute_lat = tokens * 0.003
    reroute_lat = (tokens * 0.1) * 0.005 # assuming 10% of tokens overflow and need rerouting
    return compute_lat + reroute_lat

def hardware_moe_load_balancer(tokens, num_experts):
    # Simulated latency for a dedicated hardware load balancer
    # Balances routing implicitly via a hardware token queue and priority mux
    latency = tokens * 0.0002
    return latency

def main():
    tokens = 8192
    num_experts = 64
    
    print("Running Hardware MoE Load Balancer Simulation...")
    sw_lat = software_moe_load_balancing(tokens, num_experts)
    print(f"Software Load Balancing Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_moe_load_balancer(tokens, num_experts)
    print(f"Hardware Load Balancer Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
