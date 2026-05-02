import math

def sim_software_sparse_norm(seq_len, dim):
    return seq_len * dim * 0.00005 # Software sparse norm checking

def sim_hardware_sparse_norm(seq_len, dim):
    return seq_len * dim * 0.000001 # Hardware inline sparse norm

seq_len = 8192
dim = 4096
soft = sim_software_sparse_norm(seq_len, dim)
hard = sim_hardware_sparse_norm(seq_len, dim)
speedup = soft / hard

print(f"Software Sparse Norm Latency: {soft:.2f} ms")
print(f"HW Sparse Norm Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
