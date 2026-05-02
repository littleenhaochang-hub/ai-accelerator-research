import time
def simulate_prefix_cache_tree_walker(context_length):
    print(f"Simulating Hardware Prefix Cache Tree Walker for {context_length} tokens...")
    sw_latency = context_length * 0.005 # Software Radix tree walk
    hw_latency = context_length * 0.0001 # HW MMU walk
    speedup = sw_latency / hw_latency
    print(f"SW Latency: {sw_latency:.4f} s")
    print(f"HW Latency: {hw_latency:.4f} s")
    print(f"Speedup: {speedup:.2f}x")
    return speedup

simulate_prefix_cache_tree_walker(64000)
