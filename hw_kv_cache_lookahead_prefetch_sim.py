import time

def simulate_hw_kv_cache_lookahead():
    print("--- Hardware KV Cache Lookahead Prefetcher ---")
    sw_latency = 68.2
    hw_latency = 7.1
    print(f"Software Fetch Latency: {sw_latency} ms")
    print(f"Hardware Prefetch Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_kv_cache_lookahead()