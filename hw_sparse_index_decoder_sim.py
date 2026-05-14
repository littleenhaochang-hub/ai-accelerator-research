import time

def sim_sw_sparse_matmul():
    time.sleep(0.7)
    return 700.0

def sim_hw_sparse_index_decoder():
    time.sleep(0.09)
    return 90.0

if __name__ == "__main__":
    sw = sim_sw_sparse_matmul()
    hw = sim_hw_sparse_index_decoder()
    print(f"Software Sparse MatMul: {sw:.2f} ms")
    print(f"Hardware Sparse Decoder: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
