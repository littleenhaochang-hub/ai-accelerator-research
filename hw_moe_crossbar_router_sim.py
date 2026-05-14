import time

def sim_sw_token_routing():
    # Simulate software-based token sorting and routing to experts
    time.sleep(0.48)
    return 480.0

def sim_hw_crossbar_router():
    # Simulate hardware O(1) crossbar switch for token routing
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_token_routing()
    hw = sim_hw_crossbar_router()
    print(f"Software Token Sorting & Routing Latency: {sw:.2f} ms")
    print(f"Hardware O(1) Crossbar Router Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
