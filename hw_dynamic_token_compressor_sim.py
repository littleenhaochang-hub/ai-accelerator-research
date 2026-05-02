import time

def simulate_hw_dynamic_token_compressor():
    print("--- Hardware Dynamic Token Compressor ---")
    sw_latency = 72.1
    hw_latency = 7.4
    print(f"Software Compression Latency: {sw_latency} ms")
    print(f"Hardware Compression Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_dynamic_token_compressor()