import time

def sim_sw_layer_norm():
    # Simulate software calculating variance (pass 1) and normalizing (pass 2)
    time.sleep(0.38)
    return 380.0

def sim_hw_inline_rmsnorm():
    # Simulate inline hardware RMSNorm calculating variance on-the-fly and normalizing
    time.sleep(0.035)
    return 35.0

if __name__ == "__main__":
    sw = sim_sw_layer_norm()
    hw = sim_hw_inline_rmsnorm()
    print(f"Software 2-Pass RMSNorm Latency: {sw:.2f} ms")
    print(f"Hardware Inline 1-Pass RMSNorm Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
