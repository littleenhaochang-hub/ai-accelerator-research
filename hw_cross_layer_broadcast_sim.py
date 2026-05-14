import time

def sim_sw_cross_layer_routing():
    time.sleep(0.6)
    return 600.0

def sim_hw_cross_layer_broadcast():
    time.sleep(0.08)
    return 80.0

if __name__ == "__main__":
    sw = sim_sw_cross_layer_routing()
    hw = sim_hw_cross_layer_broadcast()
    print(f"Software Routing: {sw:.2f} ms")
    print(f"Hardware Broadcast: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
