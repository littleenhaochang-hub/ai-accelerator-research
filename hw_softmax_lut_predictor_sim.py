import time

def sim_software_softmax():
    # Simulate CPU/FPU based softmax for 8K context
    time.sleep(0.35)
    return 350.0

def sim_hardware_softmax_lut():
    # Simulate Hardware PWL LUT based softmax
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_software_softmax()
    hw = sim_hardware_softmax_lut()
    print(f"Software Softmax Latency: {sw:.2f} ms")
    print(f"Hardware LUT Softmax Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
