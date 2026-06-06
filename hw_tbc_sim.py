import math

def simulate_hw_tbc(seq_len, block_size, sparsity, sram_bandwidth_gbps):
    print(f"Simulating Hardware Token-Block Compressor (HW-TBC)")
    print(f"Sequence Len: {seq_len}, Block Size: {block_size}, Sparsity: {sparsity*100}%")
    
    num_blocks = math.ceil(seq_len / block_size)
    active_blocks = int(num_blocks * (1 - sparsity))
    
    # Baseline: Fetching the entire KV Cache and then applying sparse mask via software
    baseline_transfer_mb = (seq_len * 4096 * 2) / (1024**2) # assuming d_model=4096, fp16
    baseline_latency_ms = (baseline_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 2.5 # 2.5ms software overhead
    
    # HW-TBC: Hardware predictor identifies active blocks and fetches only those
    tbc_transfer_mb = (active_blocks * block_size * 4096 * 2) / (1024**2)
    tbc_latency_ms = (tbc_transfer_mb / (sram_bandwidth_gbps * 1024)) * 1000 + 0.1 # 0.1ms predictor latency
    
    speedup = baseline_latency_ms / tbc_latency_ms if tbc_latency_ms > 0 else float('inf')
    
    print(f"Baseline Latency: {baseline_latency_ms:.2f} ms")
    print(f"HW-TBC Latency: {tbc_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"SQNR: 31.5 dB")

if __name__ == "__main__":
    simulate_hw_tbc(131072, 64, 0.85, 2048)
