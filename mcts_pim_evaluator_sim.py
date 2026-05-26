import time
import math

def simulate_ttc_mcts_pim(nodes=512, state_size_mb=2):
    # Baseline: CPU/GPU memory ping-pong for MCTS node evaluation
    pcie_latency_ms = 0.05
    baseline_latency = nodes * pcie_latency_ms * 2 # read/write
    
    # Proposed: In-SRAM PIM (Processing-in-Memory) MCTS Evaluator
    pim_latency_ms = 0.001
    proposed_latency = nodes * pim_latency_ms
    
    speedup = baseline_latency / proposed_latency
    print(f"Nodes: {nodes}, State Size: {state_size_mb}MB")
    print(f"Baseline Latency (PCIe): {baseline_latency:.2f} ms")
    print(f"Proposed Latency (PIM): {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_ttc_mcts_pim()
