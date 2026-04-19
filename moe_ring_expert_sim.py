import math

def simulate_moe_ring(num_npus=8, expert_size_gb=2.0, bandwidth_gbps=100.0, ring_latency_ms=0.5, tokens_per_npu=32):
    print("=== MoE Expert Ring Interconnect Hardware Simulation ===")
    print(f"NPUs: {num_npus}, Expert Size: {expert_size_gb}GB, Ring Bandwidth: {bandwidth_gbps}GB/s")
    
    # Baseline: Hub-and-Spoke (All-to-All or CPU-bottlenecked)
    # Assume worst case: all NPUs need an expert from the CPU or a single bottlenecked node
    hub_spoke_transfer_time = (expert_size_gb / bandwidth_gbps) * num_npus * 1000 # ms
    
    # Ring Interconnect: Pipelined expert passing
    # Experts shift 1 step per cycle. Max distance is num_npus / 2
    ring_step_time = (expert_size_gb / bandwidth_gbps) * 1000 + ring_latency_ms
    max_ring_steps = math.ceil(num_npus / 2)
    ring_transfer_time = ring_step_time * max_ring_steps
    
    print(f"Hub-and-Spoke Max Transfer Time: {hub_spoke_transfer_time:.2f} ms")
    print(f"Ring Interconnect Max Transfer Time: {ring_transfer_time:.2f} ms")
    
    speedup = hub_spoke_transfer_time / ring_transfer_time
    print(f"Speedup: {speedup:.2f}x")
    
    if speedup > 1.5:
        print("Conclusion: Ring Interconnect heavily mitigates PCIe/CPU MoE bottlenecks.")
    else:
        print("Conclusion: Ring bandwidth insufficient.")

if __name__ == "__main__":
    simulate_moe_ring()
