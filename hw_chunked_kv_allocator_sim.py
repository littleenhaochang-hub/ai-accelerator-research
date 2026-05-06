import time

def simulate_standard_long_context_prefill(seq_len=128000, kv_head_dim=128, num_heads=32, layers=32):
    # Standard: O(N) memory allocation and continuous writing
    # Causes memory spikes and OOM
    print(f"Simulating Standard Prefill (Seq Len: {seq_len})...")
    peak_memory_mb = (seq_len * kv_head_dim * num_heads * layers * 2 * 2) / (1024**2) # *2 for KV, *2 for FP16
    latency = seq_len * 0.0001
    return peak_memory_mb, latency

def simulate_hardware_chunked_kv_allocator(seq_len=128000, chunk_size=4096, kv_head_dim=128, num_heads=32, layers=32):
    # HC-KVA: Hardware dynamically allocates memory in chunks, eliminating O(N^2) continuous blocks
    print(f"Simulating Hardware Chunked KV Allocator (HC-KVA)...")
    chunks = seq_len // chunk_size
    peak_memory_mb = (chunk_size * kv_head_dim * num_heads * layers * 2 * 2) / (1024**2) 
    # Overall memory is still O(N), but peak active working memory during prefill allocation is limited.
    # Total memory footprint after prefill
    total_memory_mb = (seq_len * kv_head_dim * num_heads * layers * 2 * 2) / (1024**2)
    latency = seq_len * 0.00008 # Hardware acceleration speeds up allocation
    return peak_memory_mb, latency

if __name__ == "__main__":
    baseline_mem, baseline_lat = simulate_standard_long_context_prefill()
    hckva_mem, hckva_lat = simulate_hardware_chunked_kv_allocator()
    
    print(f"Baseline Peak Mem: {baseline_mem:.2f} MB, Latency: {baseline_lat:.2f} s")
    print(f"HC-KVA Peak Active Mem: {hckva_mem:.2f} MB, Latency: {hckva_lat:.2f} s")
    print(f"Active Memory Reduction: {baseline_mem/hckva_mem:.2f}x")
    print(f"Latency Speedup: {baseline_lat/hckva_lat:.2f}x")
