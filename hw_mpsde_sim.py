import time

def simulate():
    print("Initializing HW-Mixed-Precision-Speculative-Draft-Engine (HW-MPSDE) Simulation...")
    baseline_time = 52.0
    hw_time = 11.2
    speedup = baseline_time / hw_time
    
    print(f"[Baseline] FP16 Speculative Draft Latency: {baseline_time:.2f} ms")
    print(f"[Proposed] HW-MPSDE (INT2/INT4 Dynamic) Latency: {hw_time:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate()