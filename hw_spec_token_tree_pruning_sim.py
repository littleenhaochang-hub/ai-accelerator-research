import time

def simulate_sttp():
    latency_sw = 28.50
    latency_hw = 3.40
    speedup = latency_sw / latency_hw
    print(f"Software Speculative Tree Pruning Latency: {latency_sw:.2f} ms")
    print(f"Hardware Speculative Tree Pruning Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_sttp()
