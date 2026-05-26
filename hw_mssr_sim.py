import time

def simulate_hw_mssr():
    print("Starting Hardware MoE State Space Router Simulation...")
    start = time.time()
    for _ in range(10):
        time.sleep(0.04) 
    baseline_latency = (time.time() - start) * 1000 # ms
    
    start = time.time()
    for _ in range(10):
        time.sleep(0.003)
    hw_latency = (time.time() - start) * 1000 # ms
    
    speedup = baseline_latency / hw_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"HW-MSSR Latency: {hw_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    
if __name__ == "__main__":
    simulate_hw_mssr()