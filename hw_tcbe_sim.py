import time

def simulate_hw_tcbe(context_length=65536, sparsity=0.85):
    print(f"Simulating Hardware Tensor-Core Bypass Engine (HW-TCBE)...")
    print(f"Context: {context_length} tokens, Sparsity: {sparsity}")
    
    # Dense MAC execution latency
    dense_latency_ms = (context_length / 1000) * 1.5 
    
    # HW-TCBE latency (bypassing zero/sparse blocks dynamically)
    hw_latency_ms = (context_length / 1000) * 1.5 * (1 - sparsity) + 0.02
    
    speedup = dense_latency_ms / hw_latency_ms
    
    print(f"Dense MAC Latency: {dense_latency_ms:.2f} ms")
    print(f"HW-TCBE Latency: {hw_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_tcbe()
