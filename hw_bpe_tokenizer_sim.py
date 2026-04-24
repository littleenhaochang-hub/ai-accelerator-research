import time

def simulate_hw_bpe_tokenizer():
    print("Simulating Hardware BPE Tokenizer vs CPU for Edge Agentic AI...")
    
    # 32K context of DOM/HTML text (approx 100K characters)
    characters = 100000
    
    # CPU BPE Tokenization (Software)
    # Cache misses, branch mispredictions, memory random access for Hash Maps
    cpu_cycles_per_char = 150 # Software overhead
    cpu_freq_mhz = 3000
    cpu_latency_ms = (characters * cpu_cycles_per_char) / (cpu_freq_mhz * 1000)
    
    # Hardware BPE Tokenizer (Parallel Trie-Walker in NPU SRAM)
    # Hardware state machine walks the Trie structure with zero branch penalty
    hw_cycles_per_char = 3 
    hw_freq_mhz = 1000 # NPU clock
    hw_latency_ms = (characters * hw_cycles_per_char) / (hw_freq_mhz * 1000)
    
    speedup = cpu_latency_ms / hw_latency_ms
    
    print(f"Text Input Length: {characters} characters")
    print(f"CPU Software Tokenizer Latency: {cpu_latency_ms:.2f} ms")
    print(f"Hardware NPU Tokenizer Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print("Conclusion: A Hardware Trie-Walker for BPE completely eliminates the CPU bottleneck before Prefill.")

if __name__ == '__main__':
    simulate_hw_bpe_tokenizer()
