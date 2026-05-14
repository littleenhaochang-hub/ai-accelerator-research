import time

def sim_sw_spec_rollback():
    # Simulate software traversing a 1024-token draft tree to rollback KV pointers
    time.sleep(0.51)
    return 510.0

def sim_hw_shadow_rollback():
    # Simulate hardware restoring KV base pointers from shadow registers in 1 clock cycle
    time.sleep(0.0001)
    return 0.1

if __name__ == "__main__":
    sw = sim_sw_spec_rollback()
    hw = sim_hw_shadow_rollback()
    print(f"Software Pointer Rollback: {sw:.2f} ms")
    print(f"Hardware Shadow Register Rollback: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
