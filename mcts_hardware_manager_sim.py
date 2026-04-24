def simulate_mcts_hardware():
    print("=== Test-Time Compute: MCTS Hardware Manager ===")
    
    nodes_expanded = 2048
    pcie_latency_per_node_ms = 0.4
    npu_eval_latency_ms = 1.5
    
    # Baseline: CPU manages tree, sends states via PCIe to NPU
    cpu_total_latency = nodes_expanded * (pcie_latency_per_node_ms + npu_eval_latency_ms)
    
    # Proposed: NPU has an embedded MCTS Tree Manager in SRAM
    sram_mcts_overhead_ms = 0.02
    hw_total_latency = nodes_expanded * (sram_mcts_overhead_ms + npu_eval_latency_ms)
    
    speedup = cpu_total_latency / hw_total_latency
    
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"CPU MCTS Latency: {cpu_total_latency:.2f} ms")
    print(f"Hardware MCTS Latency: {hw_total_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_mcts_hardware()
