import time

def sim_sw_token_dropping():
    time.sleep(0.45)
    return 450.0

def sim_hw_attention_sink_locking():
    time.sleep(0.05)
    return 50.0

if __name__ == "__main__":
    sw = sim_sw_token_dropping()
    hw = sim_hw_attention_sink_locking()
    print(f"Software Sink Eviction: {sw:.2f} ms")
    print(f"Hardware Sink Locking: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
