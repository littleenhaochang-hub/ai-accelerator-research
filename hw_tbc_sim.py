import time

def simulate_hw_tbc(vocab_size=128000):
    print(f"Simulating Hardware Token-Byte Compressor (HW-TBC)...")
    
    # Software latency: BPE encoding/decoding overhead per token
    sw_latency_ms = (vocab_size / 1000) * 0.15 
    
    # Hardware latency: Inline Trie walker and byte-packer
    hw_latency_ms = (vocab_size / 1000) * 0.012
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software BPE Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-TBC Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_tbc()
