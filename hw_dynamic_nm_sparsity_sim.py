import time

def sim_sw_dynamic_sparsity():
    # Simulate CPU/GPU software evaluating token importance and switching sparsity kernels
    time.sleep(0.40)
    return 400.0

def sim_hw_dynamic_sparsity_controller():
    # Simulate dedicated hardware controller instantly switching N:M sparsity masks for MAC array
    time.sleep(0.045)
    return 45.0

if __name__ == "__main__":
    sw = sim_sw_dynamic_sparsity()
    hw = sim_hw_dynamic_sparsity_controller()
    print(f"Software Dynamic Sparsity Latency: {sw:.2f} ms")
    print(f"Hardware N:M Sparsity Controller Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
