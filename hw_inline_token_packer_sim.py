import time

def sim_sw_token_packing():
    # Simulate software traversing token masks and packing active tokens into contiguous memory
    time.sleep(0.58)
    return 580.0

def sim_hw_token_packer():
    # Simulate inline hardware DMA token packer filtering tokens on-the-fly
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_token_packing()
    hw = sim_hw_token_packer()
    print(f"Software Token Packing Latency: {sw:.2f} ms")
    print(f"Hardware Inline Token Packer Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
