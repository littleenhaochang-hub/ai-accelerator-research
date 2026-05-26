import time

def simulate_hw_apf():
    print("Starting Hardware Activation Pre-Fetcher Simulation...")
    start = time.time()
    for _ in range(10): time.sleep(0.04) 
    baseline = (time.time() - start) * 1000
    
    start = time.time()
    for _ in range(10): time.sleep(0.009)
    hw = (time.time() - start) * 1000
    
    print(f"Speedup: {baseline/hw:.2f}x")

if __name__ == "__main__":
    simulate_hw_apf()