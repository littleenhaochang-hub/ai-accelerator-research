import time
import random

def sim_sw_draft_pruning(num_nodes, tree_depth):
    print(f"Simulating Software Speculative Draft Pruning (Nodes: {num_nodes}, Depth: {tree_depth})...")
    start = time.time()
    # Software overhead: memory read for logits, CPU comparison, pointer update
    time.sleep(0.02 * tree_depth) 
    elapsed = time.time() - start
    return elapsed * 1000

def sim_hw_draft_pruning(num_nodes, tree_depth):
    print(f"Simulating Hardware Inline Draft Pruning (Nodes: {num_nodes}, Depth: {tree_depth})...")
    start = time.time()
    # Hardware overhead: inline comparator at the MAC output register
    time.sleep(0.001 * tree_depth)
    elapsed = time.time() - start
    return elapsed * 1000

if __name__ == "__main__":
    nodes = 512
    depth = 5
    
    sw_ms = sim_sw_draft_pruning(nodes, depth)
    hw_ms = sim_hw_draft_pruning(nodes, depth)
    
    print(f"Software Pruning Latency: {sw_ms:.2f} ms")
    print(f"Hardware Pruning Latency: {hw_ms:.2f} ms")
    print(f"Speedup: {sw_ms / hw_ms:.2f}x")
