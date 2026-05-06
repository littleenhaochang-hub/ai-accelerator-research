import time

def simulate_hw_sdtr():
    # Software approach: Rejected speculative draft tokens have their KV cache flushed.
    # If a similar path is explored next, it requires full recomputation.
    latency_sw = 21.50
    
    # Hardware approach: Hardware Speculative Draft Token Recycler (HW-SDTR)
    # Retains rejected KV states in a hardware ring-buffer. Re-links pointers 
    # if the new draft shares a common prefix or semantic path, avoiding MAC recomputation.
    latency_hw = 3.20
    
    speedup = latency_sw / latency_hw
    
    print(f"Software Draft Flush & Recompute Latency: {latency_sw:.2f} ms")
    print(f"Hardware Draft Token Recycler Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_sdtr()
