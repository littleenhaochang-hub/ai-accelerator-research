import math

def sim_software_context_compression(seq_len):
    return seq_len * 0.015 # Software pooling/summarization

def sim_hardware_context_compression(seq_len):
    return seq_len * 0.0003 # Hardware inline sliding window pooling

seq_len = 262144 # 256K context
soft = sim_software_context_compression(seq_len)
hard = sim_hardware_context_compression(seq_len)
speedup = soft / hard

print(f"Software Context Compression Latency: {soft:.2f} ms")
print(f"HW Context Compression Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
