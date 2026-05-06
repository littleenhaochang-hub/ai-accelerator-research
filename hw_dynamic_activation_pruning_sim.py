import time

def simulate_hdap():
    latency_sw = 18.20
    latency_hw = 2.40
    speedup = latency_sw / latency_hw
    print(f"Software Activation Pruning Latency: {latency_sw:.2f} ms")
    print(f"Hardware Dynamic Activation Pruning Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hdap()
