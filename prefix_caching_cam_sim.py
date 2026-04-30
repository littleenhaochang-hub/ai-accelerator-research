import math

def sim_soft_prefix_matching(seq_len):
    return seq_len * 0.015

def sim_hard_prefix_cam(seq_len):
    return seq_len * 0.001

seq_len = 32768
soft = sim_soft_prefix_matching(seq_len)
hard = sim_hard_prefix_cam(seq_len)
speedup = soft / hard

print(f"Software Prefix Matching Latency: {soft:.2f} ms")
print(f"HW Prefix CAM Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
