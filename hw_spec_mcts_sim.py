import time
import math

def simulate_hw_spec_mcts(nodes_evaluated=1024):
    # Baseline: CPU runs MCTS expansion and delegates node evaluation to NPU/GPU sequentially
    cpu_npu_sync_ms = 0.1 
    software_latency_ms = nodes_evaluated * cpu_npu_sync_ms 
    
    # Proposed: Hardware Speculative MCTS Co-Processor (HW-SMCTS)
    # The NPU autonomously manages the MCTS tree in SRAM and dispatches MAC operations inline
    hardware_latency_ms = nodes_evaluated * 0.002
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"MCTS Nodes Evaluated: {nodes_evaluated}")
    print(f"Baseline Latency (CPU-NPU Sync): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SMCTS): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_spec_mcts()
