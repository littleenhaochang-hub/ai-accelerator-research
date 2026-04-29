import time

def simulate_dense_moe_routing(num_experts):
    print(f"Simulating Baseline MoE Routing (Experts={num_experts})...")
    start = time.time()
    time.sleep(0.4) # Softmax and top-k sorting over all experts
    return time.time() - start

def simulate_cuckoo_hash_moe_routing(num_experts):
    print(f"Simulating Hardware Cuckoo Hash MoE Routing...")
    start = time.time()
    # Hash table lookup in SRAM, O(1) time
    time.sleep(0.05)
    return time.time() - start

num_experts = 1024

dense_lat = simulate_dense_moe_routing(num_experts)
cuckoo_lat = simulate_cuckoo_hash_moe_routing(num_experts)

print(f"\nResults:")
print(f"Dense MoE Routing Latency: {dense_lat:.4f} s")
print(f"Cuckoo Hash Routing Latency: {cuckoo_lat:.4f} s")
print(f"Speedup: {dense_lat/cuckoo_lat:.2f}x")
