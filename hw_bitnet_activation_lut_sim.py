import time

def sim_sw_bitnet_activation():
    # Simulate CPU/GPU handling non-linear activation and thresholding for BitNet
    time.sleep(0.38)
    return 380.0

def sim_hw_bitnet_activation_lut():
    # Simulate zero-MAC Hardware LUT for BitNet b1.58 activation & thresholding
    time.sleep(0.035)
    return 35.0

if __name__ == "__main__":
    sw = sim_sw_bitnet_activation()
    hw = sim_hw_bitnet_activation_lut()
    print(f"Software BitNet Activation Latency: {sw:.2f} ms")
    print(f"Hardware LUT Activation Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
