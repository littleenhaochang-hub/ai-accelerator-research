import math

def sim_standard_gqa_fetch(seq_len, num_groups):
    return seq_len * num_groups * 0.02

def sim_hw_gqa_mmu(seq_len, num_groups):
    return seq_len * 1 * 0.022 + seq_len * 0.001

seq_len = 32768
num_groups = 8

soft = sim_standard_gqa_fetch(seq_len, num_groups)
hard = sim_hw_gqa_mmu(seq_len, num_groups)
speedup = soft / hard

print(f"Standard GQA Latency: {soft:.2f} ms")
print(f"HW GQA MMU Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
