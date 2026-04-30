import math

def sim_software_pos_embed(seq_len):
    return seq_len * 0.003 # Software RoPE or Alibi calculation

def sim_hardware_pos_embed(seq_len):
    return seq_len * 0.0001 # Hardware inline position embedding generation

seq_len = 65536
soft = sim_software_pos_embed(seq_len)
hard = sim_hardware_pos_embed(seq_len)
speedup = soft / hard

print(f"Software Position Embed Latency: {soft:.2f} ms")
print(f"HW Position Embed Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
