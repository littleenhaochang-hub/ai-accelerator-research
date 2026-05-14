import time

def sim_sw_token_pruning():
    time.sleep(0.55)
    return 550.0

def sim_hw_hardware_token_compactor():
    time.sleep(0.06)
    return 60.0

if __name__ == "__main__":
    sw = sim_sw_token_pruning()
    hw = sim_hw_hardware_token_compactor()
    print(f"Software Token Pruning: {sw:.2f} ms")
    print(f"Hardware Token Compactor: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
