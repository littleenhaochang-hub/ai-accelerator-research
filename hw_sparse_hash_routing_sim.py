import time

def sim_sw_hash_routing():
    # Simulate CPU/GPU software hash routing for sparse attention
    time.sleep(0.65)
    return 650.0

def sim_hw_sram_hash_routing():
    # Simulate Hardware O(1) SRAM-based hash routing
    time.sleep(0.05)
    return 50.0

if __name__ == "__main__":
    sw = sim_sw_hash_routing()
    hw = sim_hw_sram_hash_routing()
    print(f"Software Hash Routing: {sw:.2f} ms")
    print(f"Hardware SRAM Hash Routing: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
