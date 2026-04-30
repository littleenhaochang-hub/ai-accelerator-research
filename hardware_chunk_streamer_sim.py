import math

def sim_software_chunking(seq_len):
    # O(N^2) overhead for managing chunks in software
    return seq_len * 0.008

def sim_hardware_chunking(seq_len):
    # O(N) inline hardware chunk streaming
    return seq_len * 0.0002

seq_len = 1048576 # 1M context
soft = sim_software_chunking(seq_len)
hard = sim_hardware_chunking(seq_len)
speedup = soft / hard

print(f"Software Chunking Latency: {soft:.2f} ms")
print(f"HW Chunking Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
