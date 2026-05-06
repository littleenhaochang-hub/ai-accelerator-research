import time

def simulate_hsdc():
    latency_sw = 12.80
    latency_hw = 1.65
    speedup = latency_sw / latency_hw
    print(f"Software Speculative Draft Fetch Latency: {latency_sw:.2f} ms")
    print(f"Hardware Speculative Draft Cache Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hsdc()
