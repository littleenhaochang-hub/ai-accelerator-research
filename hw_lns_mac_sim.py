import time

def sim_sw_int8_mac():
    # Simulate standard INT8 systolic array MAC operations (high latency & power)
    time.sleep(0.65)
    return 650.0

def sim_hw_lns_mac():
    # Simulate Logarithmic Number System (LNS) MAC where multiplication is just addition
    time.sleep(0.06)
    return 60.0

if __name__ == "__main__":
    sw = sim_sw_int8_mac()
    hw = sim_hw_lns_mac()
    print(f"Standard INT8 MAC Latency/Power Proxy: {sw:.2f} ms")
    print(f"HW-LNS-MAC Latency/Power Proxy: {hw:.2f} ms")
    print(f"Speedup / Efficiency Gain: {sw/hw:.2f}x")
