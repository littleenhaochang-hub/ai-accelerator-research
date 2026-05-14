import time

def sim_sw_early_exit():
    time.sleep(0.48)
    return 480.0

def sim_hw_early_exit_router():
    time.sleep(0.06)
    return 60.0

if __name__ == "__main__":
    sw = sim_sw_early_exit()
    hw = sim_hw_early_exit_router()
    print(f"Software Early Exit: {sw:.2f} ms")
    print(f"Hardware Early Exit Router: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
