import time
import numpy as np

def sim_software_tree_routing(num_tokens, tree_depth):
    print(f"Simulating Software Token-Tree Routing (Tokens: {num_tokens}, Depth: {tree_depth})...")
    start = time.time()
    # O(N) memory pointer chasing for tree traversal
    for _ in range(num_tokens):
        time.sleep(0.0001 * tree_depth) # Simulate cache misses
    elapsed = time.time() - start
    return elapsed * 1000

def sim_hardware_tree_routing(num_tokens, tree_depth):
    print(f"Simulating Hardware O(1) Token-Tree Routing (Tokens: {num_tokens}, Depth: {tree_depth})...")
    start = time.time()
    # O(1) TCAM-based routing
    time.sleep(0.0005) # Fixed hardware latency overhead
    elapsed = time.time() - start
    return elapsed * 1000

if __name__ == "__main__":
    tokens = 1024
    depth = 8
    
    sw_ms = sim_software_tree_routing(tokens, depth)
    hw_ms = sim_hardware_tree_routing(tokens, depth)
    
    print(f"Software Routing Latency: {sw_ms:.2f} ms")
    print(f"Hardware TCAM Routing Latency: {hw_ms:.2f} ms")
    print(f"Speedup: {sw_ms / hw_ms:.2f}x")
