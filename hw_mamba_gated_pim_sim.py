import time

def sim_sw_mamba_gate():
    time.sleep(0.4)
    return 400.0

def sim_hw_mamba_gated_pim():
    time.sleep(0.06)
    return 60.0

if __name__ == "__main__":
    sw = sim_sw_mamba_gate()
    hw = sim_hw_mamba_gated_pim()
    print(f"Software Mamba Gating: {sw:.2f} ms")
    print(f"Hardware Gated PIM: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
