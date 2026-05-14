import time

def sim_sw_sparse_head_eval():
    # Simulate software iterating over attention heads and applying mask/zeroing
    time.sleep(0.44)
    return 440.0

def sim_hw_dynamic_head_gating():
    # Simulate inline hardware moving-average evaluator that clock-gates inactive heads
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_sparse_head_eval()
    hw = sim_hw_dynamic_head_gating()
    print(f"Software Head Evaluation Latency: {sw:.2f} ms")
    print(f"Hardware Dynamic Head Gating Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
