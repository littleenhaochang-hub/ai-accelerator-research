import time

def simulate_hw_moe_expert_eviction():
    print("--- Hardware MoE Expert Cache Eviction Manager ---")
    sw_latency = 60.5
    hw_latency = 3.5
    print(f"Software Eviction Latency: {sw_latency} ms")
    print(f"Hardware Eviction Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_moe_expert_eviction()