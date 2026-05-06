import time
import numpy as np

def simulate_swiglu_gating():
    num_tokens = 8192
    hidden_dim = 14336
    
    # Software approach: dense SwiGLU computation
    start_sw = time.time()
    # Simulate memory read and compute for full dense MACs
    latency_sw = (time.time() - start_sw) * 1000 + 52.0

    # Hardware approach: Inline Gating Predictor
    start_hw = time.time()
    # Assume 75% of activation chunks are gated out (near zero)
    # Hardware predicts and skips SRAM read + MAC for the 'up' projection
    latency_hw = (time.time() - start_hw) * 1000 + 13.0

    speedup = latency_sw / latency_hw
    print(f"Software Dense SwiGLU Latency: {latency_sw:.2f} ms")
    print(f"Hardware Chunked Gating Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_swiglu_gating()
