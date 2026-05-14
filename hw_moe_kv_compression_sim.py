import time

def sim_software_moe_kv():
    start = time.time()
    time.sleep(0.5) # memory bound
    return (time.time() - start) * 1000

def sim_hardware_moe_kv():
    start = time.time()
    time.sleep(0.05) # compressed hardware bus
    return (time.time() - start) * 1000

if __name__ == "__main__":
    sw = sim_software_moe_kv()
    hw = sim_hardware_moe_kv()
    print(f"Software MoE KV: {sw:.2f} ms")
    print(f"Hardware MoE KV: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
