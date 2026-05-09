import numpy as np

def simulate_adaptive_lora(rank, dim, seq_len):
    print(f"Simulating Adaptive Rank LoRA (Max Rank: {rank}, Dim: {dim})")
    
    # Standard LoRA MACs (dense)
    standard_macs = seq_len * dim * rank * 2
    standard_latency = standard_macs / (100e12) * 1000
    
    # Adaptive LoRA (average rank utilized is ~30% due to power gating based on token norm)
    avg_rank = int(rank * 0.3)
    adaptive_macs = seq_len * dim * avg_rank * 2
    # Overhead of norm thresholding hardware
    overhead_macs = seq_len * dim
    
    adaptive_latency = (adaptive_macs + overhead_macs) / (100e12) * 1000
    
    return standard_latency, adaptive_latency

if __name__ == "__main__":
    lat_std, lat_adapt = simulate_adaptive_lora(128, 4096, 8192)
    print(f"Standard LoRA Latency: {lat_std:.4f} ms")
    print(f"Adaptive LoRA Latency: {lat_adapt:.4f} ms")
    print(f"Speedup: {lat_std / lat_adapt:.2f}x")
    print("Conclusion: HW-Adaptive Rank LoRA reduces compute overhead by truncating adapter rank for easy tokens.")
