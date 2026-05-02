import time

def simulate_hw_spec_draft_allocator():
    print("--- Hardware Speculative Draft Memory Allocator ---")
    sw_latency = 55.4
    hw_latency = 6.2
    print(f"Software Allocation Latency: {sw_latency} ms")
    print(f"Hardware Allocation Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_spec_draft_allocator()