import numpy as np

def simulate_hw_ssm_decay_fuser(seq_len, dim, layers=32):
    print(f"Simulating Hardware SSM Exponential Decay Fuser (HW-SEDF) - Seq: {seq_len}, Dim: {dim}")
    
    # Software SSM Scan:
    # Read State -> Compute Exp Decay (Transcendental) -> Multiply -> Add -> Write State
    # Highly memory bound due to multi-pass SRAM reads/writes for intermediate steps
    sw_passes = 3
    sw_latency = (seq_len * dim * sw_passes) / (1000e9) * 1000 # 1TB/s SRAM BW
    
    # HW-SEDF: 
    # Read State -> Inline PWL Exp() -> Inline Multiply/Add -> Write State
    # Done in a single pass (Registers only)
    hw_passes = 1
    hw_latency = (seq_len * dim * hw_passes) / (4000e9) * 1000 # 4TB/s internal bus, fused pipeline
    
    print(f"Software SSM Scan Latency: {sw_latency:.4f} ms")
    print(f"HW-SEDF Latency: {hw_latency:.4f} ms")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_ssm_decay_fuser(32768, 4096)
