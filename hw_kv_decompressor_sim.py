import time

def simulate_hw_kv_decompressor():
    print("--- Hardware Inline KV Cache Decompressor ---")
    sw_latency = 55.0
    hw_latency = 4.2
    print(f"Software Decompression Latency: {sw_latency} ms")
    print(f"Hardware Inline Decompression Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_kv_decompressor()