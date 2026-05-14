import time

def sim_sw_token_dropping():
    # Simulate software iteratively dropping tokens, updating indices, and gathering remaining tensors
    time.sleep(0.48)
    return 480.0

def sim_hw_dynamic_sparse_attention():
    # Simulate inline hardware dropping tokens at the read port with zero padding
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_token_dropping()
    hw = sim_hw_dynamic_sparse_attention()
    print(f"Software Token Dropping Overhead: {sw:.2f} ms")
    print(f"Hardware Dynamic Sparse Attention Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
