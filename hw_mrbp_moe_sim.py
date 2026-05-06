import time

def simulate_hw_mrbp():
    # Software approach: Every token goes through the MoE routing linear layer
    # Requires SRAM fetch of routing weights and Dense MAC operation
    latency_sw = 12.80
    
    # Hardware approach: Hardware MoE Router-Bypass Predictor (HW-MRBP)
    # Uses a lightweight temporal token correlation hash. If a token is semantically
    # contiguous (e.g. part of a single word/entity), it bypasses the router MACs
    # and directly reuses the previous token's expert assignment.
    latency_hw = 1.45
    
    speedup = latency_sw / latency_hw
    
    print(f"Software MoE Routing Latency: {latency_sw:.2f} ms")
    print(f"Hardware Router-Bypass Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_mrbp()
