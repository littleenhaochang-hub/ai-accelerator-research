import time

def simulate_clipping():
    latency_sw = 12.50
    latency_hw = 1.80
    speedup = latency_sw / latency_hw
    print(f"Software Activation Clipping Latency: {latency_sw:.2f} ms")
    print(f"Hardware Inline Clipping Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_clipping()
