import time

def simulate_hw_m2sfb():
    seq_len = 8192
    chunk_size = 256
    num_chunks = seq_len // chunk_size
    
    # Baseline: SRAM read/write for state passing between chunks in Mamba-2
    sram_latency_per_pass_us = 2.5 # 2.5 microseconds per state write/read roundtrip
    baseline_latency_ms = (num_chunks * sram_latency_per_pass_us) / 1000.0
    
    # HW-M2SFB: Register-level forwarding bus (0 SRAM access)
    register_latency_per_pass_us = 0.1 # 100 ns
    m2sfb_latency_ms = (num_chunks * register_latency_per_pass_us) / 1000.0
    
    print("=== HW-M2SFB Simulation ===")
    print(f"Sequence Length: {seq_len}, Chunks: {num_chunks}")
    print(f"Baseline Latency: {baseline_latency_ms:.4f} ms")
    print(f"HW-M2SFB Latency: {m2sfb_latency_ms:.4f} ms")
    print(f"Speedup: {baseline_latency_ms/m2sfb_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_m2sfb()
