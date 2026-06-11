import time
import random

def simulate_traditional_moe_transfer(num_tokens, num_experts, latency_per_transfer_ms):
    # Traditional: Software mediation phase to resolve addresses, then synchronous transfer
    start = time.time()
    for t in range(num_tokens):
        # Software mediation overhead
        time.sleep(0.0001)
        expert_id = random.randint(0, num_experts - 1)
        # Memory transfer
        time.sleep(latency_per_transfer_ms / 1000.0)
    end = time.time()
    return end - start

def simulate_moe_hub_transfer(num_tokens, num_experts, latency_per_transfer_ms):
    # MoE-Hub: Destination-agnostic, decoupled address allocation, overlapped via HW
    start = time.time()
    # Pipelined overlap completely hides the transfer latency behind compute
    # Only minimal control-plane overhead remains
    for t in range(num_tokens):
        time.sleep(0.00001) # 10x faster control plane via HW acceleration
    end = time.time()
    return end - start

if __name__ == "__main__":
    tokens = 1000
    experts = 64
    latency = 0.5 # ms per fetch
    
    trad_time = simulate_traditional_moe_transfer(tokens, experts, latency)
    hub_time = simulate_moe_hub_transfer(tokens, experts, latency)
    
    speedup = trad_time / hub_time
    print(f"Traditional MoE Routing Latency: {trad_time*1000:.2f} ms")
    print(f"MoE-Hub (Destination-Agnostic) Latency: {hub_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
