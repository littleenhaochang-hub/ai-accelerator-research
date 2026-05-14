import time

def sim_sw_allgather():
    # CPU orchestrated PCIe All-Gather for Tensor Parallelism
    time.sleep(0.7)
    return 700.0

def sim_hw_allgather():
    # Dedicated Hardware All-Gather Engine (Zero-Copy P2P)
    time.sleep(0.07)
    return 70.0

if __name__ == "__main__":
    sw = sim_sw_allgather()
    hw = sim_hw_allgather()
    print(f"Software All-Gather: {sw:.2f} ms")
    print(f"Hardware All-Gather: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
