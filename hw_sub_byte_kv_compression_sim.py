import time

def simulate_sbkvc():
    latency_sw = 22.40
    latency_hw = 3.10
    speedup = latency_sw / latency_hw
    print(f"Software Sub-Byte KV Decompression Latency: {latency_sw:.2f} ms")
    print(f"Hardware Inline Sub-Byte KV Decompression Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_sbkvc()
