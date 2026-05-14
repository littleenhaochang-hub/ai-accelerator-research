import time
import math

def simulate_prefill_oom(context_length, use_chunking):
    print(f"Simulating Prefill for {context_length} tokens. Chunking: {use_chunking}")
    start_time = time.time()
    
    # Simulate memory allocation and computation
    if use_chunking:
        chunk_size = 4096
        num_chunks = math.ceil(context_length / chunk_size)
        peak_memory_mb = 0
        total_latency = 0
        
        for i in range(num_chunks):
            # Process chunk
            current_chunk_size = min(chunk_size, context_length - i * chunk_size)
            # Memory scales with chunk_size * current_context (linear-ish for KV, quadratic for chunk attention)
            # Simplified:
            chunk_mem = (current_chunk_size * current_chunk_size * 2) / (1024 * 1024) # MB
            kv_mem = ((i + 1) * chunk_size * 2 * 128) / (1024 * 1024) # MB
            
            current_peak = chunk_mem + kv_mem
            peak_memory_mb = max(peak_memory_mb, current_peak)
            
            # Latency
            total_latency += (current_chunk_size * 0.0001)
            
    else:
        # Without chunking, full O(N^2) memory footprint
        peak_memory_mb = (context_length * context_length * 2) / (1024 * 1024) # MB
        kv_mem = (context_length * 2 * 128) / (1024 * 1024) # MB
        peak_memory_mb += kv_mem
        
        total_latency = (context_length * 0.0001)

    print(f"Peak Memory: {peak_memory_mb:.2f} MB")
    print(f"Total Latency: {total_latency:.4f} s")
    return peak_memory_mb, total_latency

# Simulate 128K context
context_len = 128 * 1024
base_mem, base_lat = simulate_prefill_oom(context_len, False)
chunk_mem, chunk_lat = simulate_prefill_oom(context_len, True)

print(f"Memory Reduction: {base_mem / chunk_mem:.2f}x")
