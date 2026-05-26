import time

def simulate_hw_imks(context_length=2000000):
    print(f"Simulating Hardware In-Memory KV Searcher (HW-IMKS)...")
    print(f"Context: {context_length} tokens")
    
    # Software latency: fetching KV blocks over memory bus to MACs
    sw_latency_ms = (context_length / 1000) * 2.8 
    
    # Hardware latency: Processing-In-Memory (PIM) evaluation of attention scores
    hw_latency_ms = (context_length / 1000) * 0.035
    
    speedup = sw_latency_ms / hw_latency_ms
    
    print(f"Software KV Search Latency: {sw_latency_ms:.2f} ms")
    print(f"HW-IMKS Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_imks()
