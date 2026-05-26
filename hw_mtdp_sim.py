import time

def simulate_hw_mtdp(tokens=8192, drop_ratio=0.15):
    # Baseline: Software routing drops tokens AFTER computing dense router logits and sorting
    software_latency_ms = tokens * 0.012 
    
    # Proposed: Hardware MoE Token-Drop Predictor (HW-MTDP)
    # Uses a lightweight INT2 predictor before the main router to identify and drop doomed tokens instantly
    hardware_latency_ms = (tokens * (1 - drop_ratio)) * 0.012 + (tokens * 0.001)
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Tokens: {tokens}, Drop Ratio: {drop_ratio}")
    print(f"Baseline Latency (Software Drop): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-MTDP): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_mtdp()
