import math

def sim_software_group_gemm(layers, batch_size):
    return layers * batch_size * 0.005 # Software CUDA/NPU stream launch overhead

def sim_hardware_group_gemm(layers, batch_size):
    return layers * batch_size * 0.0001 # Hardware command queue unrolling

layers = 64
batch_size = 128
soft = sim_software_group_gemm(layers, batch_size)
hard = sim_hardware_group_gemm(layers, batch_size)
speedup = soft / hard

print(f"Software Group-GEMM Launch Latency: {soft:.2f} ms")
print(f"HW Group-GEMM Scheduler Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
