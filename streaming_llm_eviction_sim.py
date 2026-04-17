import numpy as np

def simulate_streaming_llm_hardware():
    print("Starting StreamingLLM Hardware Eviction Simulation...")
    
    total_generated_tokens = 100000
    window_size = 2048
    sink_size = 4
    dim = 4096
    bytes_per_element = 2 # FP16
    
    # Dense attention total memory reads (arithmetic progression)
    # SUM(1 to N)
    dense_memory_reads_elements = (total_generated_tokens * (total_generated_tokens + 1) / 2) * dim * 2
    dense_memory_reads_TB = (dense_memory_reads_elements * bytes_per_element) / 1e12
    
    # StreamingLLM total memory reads
    # For first 'window_size' tokens, it's dense. After that, it's fixed at window_size + sink_size.
    initial_reads = (window_size * (window_size + 1) / 2)
    streaming_reads = (total_generated_tokens - window_size) * (window_size + sink_size)
    streaming_memory_reads_elements = (initial_reads + streaming_reads) * dim * 2
    streaming_memory_reads_TB = (streaming_memory_reads_elements * bytes_per_element) / 1e12
    
    bandwidth_reduction = 1 - (streaming_memory_reads_TB / dense_memory_reads_TB)
    
    print(f"Tokens Generated: {total_generated_tokens}")
    print(f"Dense Attention KV Reads: {dense_memory_reads_TB:.2f} TB")
    print(f"StreamingLLM KV Reads: {streaming_memory_reads_TB:.2f} TB")
    print(f"KV Memory Bandwidth Reduction: {bandwidth_reduction*100:.2f}%")
    print("Conclusion: StreamingLLM allows infinite generation without OOM. Hardware requires an 'SRAM Ring Buffer with Static Sink Roots' to automatically evict stale KV tokens natively without software overhead.")

if __name__ == "__main__":
    simulate_streaming_llm_hardware()
