import time

def sram_moe_routing(tokens, num_experts):
    # Simulated standard SRAM-based MoE routing (Softmax + Top-K sort)
    # O(N * E) compute followed by O(N * log E) sorting
    compute_lat = tokens * num_experts * 0.005
    sort_lat = tokens * 1.5 * 0.002
    return compute_lat + sort_lat

def cam_moe_routing(tokens, num_experts):
    # Simulated Content-Addressable Memory (CAM) MoE routing
    # O(1) parallel lookup per token
    lookup_lat = tokens * 0.001
    return lookup_lat

def main():
    tokens = 4096
    num_experts = 256 # DeepSeek style high expert count
    
    print("Running MoE Routing Hardware Simulation (SRAM vs CAM)...")
    sram_lat = sram_moe_routing(tokens, num_experts)
    print(f"Standard SRAM Routing Latency: {sram_lat:.2f} ms")
    
    cam_lat = cam_moe_routing(tokens, num_experts)
    print(f"Hardware CAM Routing Latency: {cam_lat:.2f} ms")
    
    speedup = sram_lat / cam_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
