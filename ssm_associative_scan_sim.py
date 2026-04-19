def simulate_associative_scan(seq_len=8192, alu_latency_ns=2.0, num_alus=256):
    print("=== SSM/Mamba Associative Scan Hardware Simulation ===")
    
    # Sequential O(N) Scan (Software baseline on standard MACs)
    seq_latency_ns = seq_len * alu_latency_ns
    
    # Parallel O(log N) Scan (Hardware Tree)
    import math
    tree_depth = math.ceil(math.log2(seq_len))
    parallel_latency_ns = tree_depth * alu_latency_ns
    
    speedup = seq_latency_ns / parallel_latency_ns
    
    print(f"Sequence Length: {seq_len}")
    print(f"Sequential Latency: {seq_latency_ns:.2f} ns")
    print(f"Parallel Tree Latency: {parallel_latency_ns:.2f} ns")
    print(f"Speedup: {speedup:.2f}x")
    
if __name__ == "__main__":
    simulate_associative_scan()
