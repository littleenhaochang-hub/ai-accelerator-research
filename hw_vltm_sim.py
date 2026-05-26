import time

def simulate_hw_vltm(tokens=4096, prune_ratio=0.75):
    # Baseline: Software-based Token Merging (ToMe) for Vision tokens
    software_latency_ms = tokens * 0.005 # Similarity computation and gathering overhead
    
    # Proposed: Hardware Vision-Language Token Merger (HW-VLTM) inline at SRAM write
    hardware_latency_ms = tokens * 0.0001
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Tokens: {tokens}, Prune Ratio: {prune_ratio}")
    print(f"Baseline Latency (Software): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-VLTM): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_vltm()
