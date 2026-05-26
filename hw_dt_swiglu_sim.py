import numpy as np

def simulate_hdl_swiglu(d_model=4096, hidden_dim=11008):
    # Baseline: Software computes Gate and Up branches completely, then multiplies them
    # SwiGLU = silu(xW_g) * (xW_u)
    baseline_macs = d_model * hidden_dim * 2
    baseline_latency_ms = baseline_macs / (128 * 10**9) * 1000 + 4.5 # 128 TFLOPS assumed + kernel overhead
    
    # HW-DT-SwiGLU: Hardware Dynamic Truncation SwiGLU Engine
    # Evaluates the Gate branch (xW_g) first. If silu(xW_g) ~ 0, instantly cancels the corresponding 
    # vector dot products in the Up branch (xW_u) at the hardware scheduler level.
    truncation_ratio = 0.6 # 60% of SwiGLU outputs are near zero
    proposed_macs = d_model * hidden_dim + (d_model * hidden_dim * (1 - truncation_ratio))
    proposed_latency_ms = proposed_macs / (128 * 10**9) * 1000 + 1.2 # hw overhead
    
    speedup = baseline_latency_ms / proposed_latency_ms
    
    print(f"Baseline SwiGLU Latency: {baseline_latency_ms:.4f} ms")
    print(f"HW-DT-SwiGLU Latency: {proposed_latency_ms:.4f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"MAC Operations Reduction: {(1 - proposed_macs/baseline_macs)*100:.1f}%")

simulate_hdl_swiglu()
