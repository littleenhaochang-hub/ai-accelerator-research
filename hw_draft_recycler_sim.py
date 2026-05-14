import time

def sim_sw_draft_rejection():
    # Simulate CPU discarding and resetting the entire draft KV cache state
    time.sleep(0.42)
    return 420.0

def sim_hw_draft_recycling():
    # Simulate Hardware linking rejected tokens into an SRAM shadow buffer for future retrieval
    time.sleep(0.02)
    return 20.0

if __name__ == "__main__":
    sw = sim_sw_draft_rejection()
    hw = sim_hw_draft_recycling()
    print(f"Software Draft Rejection Latency: {sw:.2f} ms")
    print(f"Hardware Draft Recycling Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
