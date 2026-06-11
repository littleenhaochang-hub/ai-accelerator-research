import time
import math

def simulate_traditional_softmax(seq_len):
    # Standard Softmax: Read from SRAM -> FPU Exp() -> SRAM -> Sum -> Divide
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000005) # FPU Exp() and digital MAC latency + memory round-trip
    return time.time() - start

def simulate_cim_softmax(seq_len):
    # Compute-in-Memory (CIM) Softmax (HASTILY Architecture):
    # Unified Compute and Lookup Modules (UCLMs) merge Lookup (Exp) and MAC inside SRAM.
    # Fine-grained pipelining limits memory footprint to linear dependence.
    start = time.time()
    for _ in range(seq_len):
        # Operations happen concurrently within the memory array without digital FPU stalls
        time.sleep(0.0000008) 
    return time.time() - start

if __name__ == "__main__":
    seq_length = 4096
    
    trad_time = simulate_traditional_softmax(seq_length)
    cim_time = simulate_cim_softmax(seq_length)
    
    speedup = trad_time / cim_time if cim_time > 0 else float('inf')
    
    print(f"Traditional FPU Softmax Latency: {trad_time*1000:.2f} ms")
    print(f"CIM-UCLM Softmax Latency: {cim_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
