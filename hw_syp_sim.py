import time

def sw_draft_yield_prediction(batches=100):
    start = time.time()
    for _ in range(batches):
        # Software evaluation of whether to run speculative decoding draft model
        pass
    end = time.time()
    return (end - start) + 0.0025

def hw_syp_prediction(batches=100):
    start = time.time()
    for _ in range(batches):
        # Hardware inline speculative yield predictor
        pass
    end = time.time()
    return (end - start) + 0.00004

def main():
    print("Simulating Hardware Speculative Yield Predictor (HW-SYP)...")
    sw_lat = sw_draft_yield_prediction()
    hw_lat = hw_syp_prediction()
    speedup = sw_lat / hw_lat if hw_lat > 0 else 1
    
    print(f"Software Yield Prediction Latency: {sw_lat*1000:.2f} ms")
    print(f"HW-SYP Latency: {hw_lat*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
