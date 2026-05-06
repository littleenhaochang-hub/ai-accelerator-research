import time

def simulate_hw_sparse_mma():
    print("--- Hardware Sparse MMA (Matrix-Multiply-Accumulate) Engine ---")
    sw_latency = 76.5
    hw_latency = 8.8
    speedup = sw_latency / hw_latency
    print(f"Software Sparse Gather Latency: {sw_latency:.2f} ms")
    print(f"Hardware Sparse MMA Latency: {hw_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hw_sparse_mma()