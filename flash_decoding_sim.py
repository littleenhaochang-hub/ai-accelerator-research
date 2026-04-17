import numpy as np

def simulate_flash_decoding():
    print("Starting FlashDecoding Hardware Simulation...")
    
    seq_len = 32768
    dim = 4096
    num_heads = 32
    head_dim = dim // num_heads
    batch_size = 1
    
    # Baseline Decoding: Load entire KV sequence for a single query token
    baseline_memory_reads_bytes = seq_len * dim * 2 * 2 # K and V, 2 bytes (FP16)
    
    # FlashDecoding: Split KV sequence into blocks (e.g., block size 256)
    block_size = 256
    num_blocks = seq_len // block_size
    
    # Simulate parallel processing across multiple SMs/Compute Units
    num_compute_units = 32
    blocks_per_unit = num_blocks // num_compute_units
    
    # In FlashDecoding, each unit processes its blocks and produces a partial attention output & max value
    partial_output_bytes_per_unit = head_dim * 2 # 2 bytes
    partial_max_bytes_per_unit = 2 # 2 bytes
    
    # Reduction phase: read all partials to compute final Softmax
    reduction_memory_reads_bytes = num_compute_units * (partial_output_bytes_per_unit + partial_max_bytes_per_unit)
    
    # Bandwidth simulation
    bandwidth_GBps = 200
    baseline_latency_us = (baseline_memory_reads_bytes / 1e9) / bandwidth_GBps * 1e6
    
    # Parallel latency is determined by the slowest unit + reduction
    parallel_kv_reads_bytes_per_unit = blocks_per_unit * block_size * dim * 2 * 2
    parallel_latency_us = (parallel_kv_reads_bytes_per_unit / 1e9) / bandwidth_GBps * 1e6
    reduction_latency_us = (reduction_memory_reads_bytes / 1e9) / bandwidth_GBps * 1e6
    
    flash_decoding_latency_us = parallel_latency_us + reduction_latency_us
    
    speedup = baseline_latency_us / flash_decoding_latency_us
    
    print(f"Context Length: {seq_len} tokens")
    print(f"Baseline Decoding Latency: {baseline_latency_us:.2f} us")
    print(f"FlashDecoding Latency (Parallel + Reduction): {flash_decoding_latency_us:.2f} us")
    print(f"Effective Throughput Speedup: {speedup:.2f}x")
    print("Conclusion: FlashDecoding parallelizes long-context KV cache reads across SMs. Hardware requires a 'Global Reduction Network' to efficiently aggregate partial Softmax sums from distributed SRAMs without funneling through DRAM.")

if __name__ == "__main__":
    simulate_flash_decoding()
