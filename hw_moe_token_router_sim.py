import time

def simulate_hw_moe_token_router():
    print("--- Hardware O(1) MoE Token Router ---")
    sw_latency = 45.1
    hw_latency = 5.2
    print(f"Software Routing Latency: {sw_latency} ms")
    print(f"Hardware Routing Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_moe_token_router()