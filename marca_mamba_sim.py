import time

def simulate_gpu_mamba(seq_len, dim):
    # Simulates generic GPU execution for Mamba:
    # Rigid GEMM cores struggle with element-wise and scan operations
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.000008) # Inefficient memory access and non-GEMM latency
    return time.time() - start

def simulate_marca_accelerator(seq_len, dim):
    # Simulates MARCA (Mamba Accelerator with ReConfigurable Architecture):
    # 1. Reduction alternative PE array
    # 2. Reusable nonlinear function unit via fast biased algorithms
    # 3. Buffer management maximizing sharing
    start = time.time()
    for _ in range(seq_len):
        time.sleep(0.0000008) # Reconfigurable PE executes scan/element-wise much faster
    return time.time() - start

if __name__ == "__main__":
    seq = 32768
    dim = 256
    gpu_time = simulate_gpu_mamba(seq, dim)
    marca_time = simulate_marca_accelerator(seq, dim)
    
    speedup = gpu_time / marca_time if marca_time > 0 else float('inf')
    
    print(f"GPU Baseline Latency: {gpu_time*1000:.2f} ms")
    print(f"MARCA Accelerator Latency: {marca_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
