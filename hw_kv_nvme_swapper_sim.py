import time

def simulate_hw_kv_swapper():
    print("--- Hardware NVMe KV Cache Swapper ---")
    sw_latency = 120.0
    hw_latency = 15.0
    print(f"Software OS Page Fault Swapping Latency: {sw_latency} ms")
    print(f"Hardware P2P NVMe Swapping Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_kv_swapper()