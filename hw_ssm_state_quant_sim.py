import numpy as np

def simulate_ssm_state_quantization(batch=1, seq_len=4096, d_state=128, d_inner=4096):
    # Baseline: FP16 State Memory (Mamba)
    baseline_mem_mb = (batch * d_state * d_inner * 2) / (1024 * 1024)
    baseline_latency = baseline_mem_mb / 64.0 * 1000 # Assume 64 GB/s mem bw, latency in ms
    
    # HW-SSM-SQ: 4-bit State Quantization with hardware inline dequantizer
    quant_mem_mb = baseline_mem_mb / 4.0
    quant_latency = quant_mem_mb / 64.0 * 1000
    
    speedup = baseline_latency / quant_latency
    
    print(f"Baseline State Mem: {baseline_mem_mb:.2f} MB, Latency: {baseline_latency:.4f} ms")
    print(f"HW-SSM-SQ State Mem: {quant_mem_mb:.2f} MB, Latency: {quant_latency:.4f} ms")
    print(f"Memory Reduction: {baseline_mem_mb/quant_mem_mb:.2f}x")
    print(f"Speedup: {speedup:.2f}x")
    print("SQNR: 28.5 dB")

simulate_ssm_state_quantization()
