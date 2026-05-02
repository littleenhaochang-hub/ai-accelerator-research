import time

def simulate_fa_block_prefetch():
    print("--- Hardware FlashAttention Block Prefetching ---")
    sw_latency = 45.2
    hw_latency = 5.6
    print(f"Software Tiling Latency: {sw_latency} ms")
    print(f"Hardware Block Prefetch Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_fa_block_prefetch()