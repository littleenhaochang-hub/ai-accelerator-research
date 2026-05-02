import time

def simulate_hw_chunk_attn():
    print("--- Hardware Chunked Attention Engine ---")
    sw_latency = 82.1
    hw_latency = 9.5
    print(f"Software Chunking Latency: {sw_latency} ms")
    print(f"Hardware Chunking Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_chunk_attn()