import random

def simulate_software_truncation(num_tokens, context_limit):
    # Software reads all tokens, sorts/evaluates, and truncates
    latency_ms = (num_tokens * 0.005) + (num_tokens * math.log2(num_tokens) * 0.0001) if num_tokens > 0 else 0
    return latency_ms

def simulate_hw_catt(num_tokens, context_limit):
    # Hardware Context-Aware Token Truncator: processes on-the-fly via inline SRAM filtering
    # O(N) but highly parallel and memory-bound
    latency_ms = num_tokens * 0.0002 
    return latency_ms

if __name__ == "__main__":
    import math
    num_tokens = 128000
    context_limit = 4096
    
    sw_time = simulate_software_truncation(num_tokens, context_limit)
    hw_time = simulate_hw_catt(num_tokens, context_limit)
    
    speedup = sw_time / hw_time if hw_time > 0 else 0
    
    print(f"Software Truncation Time: {sw_time:.2f} ms")
    print(f"HW-CATT Time: {hw_time:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
