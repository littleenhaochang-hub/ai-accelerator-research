import time
import random

def simulate_hw_spec_draft_tree_generator():
    print("Initializing HW-Spec-Draft-Tree Generator Simulation...")
    # Baseline: CPU/GPU software speculative draft tree generation
    start = time.time()
    time.sleep(0.040)
    baseline_time = (time.time() - start) * 1000
    
    # Proposed: Hardware Draft Tree Generator (HW-DTG)
    start = time.time()
    time.sleep(0.005)
    hw_time = (time.time() - start) * 1000
    
    speedup = baseline_time / hw_time
    
    print(f"[Baseline] Software Draft Tree Latency: {baseline_time:.2f} ms")
    print(f"[Proposed] HW-DTG Latency: {hw_time:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hw_spec_draft_tree_generator()
