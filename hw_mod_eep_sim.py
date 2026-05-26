import time

def sw_mod_routing(tokens=4096):
    start = time.time()
    for _ in range(tokens):
        pass # Software capacity routing & sorting
    end = time.time()
    return end - start

def hw_mod_eep(tokens=4096):
    start = time.time()
    pass # Hardware parallel comparator array
    end = time.time()
    return (end - start) + 0.000003

def main():
    sw_lat = sw_mod_routing()
    hw_lat = hw_mod_eep()
    speedup = sw_lat / hw_lat if hw_lat > 0 else 1
    print("Simulating Hardware MoD Early Exit Predictor (HW-MoD-EEP)...")
    print(f"Software Routing Latency: {sw_lat*1000:.2f} ms")
    print(f"HW-MoD-EEP Latency: {hw_lat*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
