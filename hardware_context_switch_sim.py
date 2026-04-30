import math

def sim_software_context_switch(seq_len):
    return seq_len * 0.005 # Software state save/restore overhead

def sim_hardware_context_switch(seq_len):
    return seq_len * 0.0001 # Hardware background register shadowing

seq_len = 16384
soft = sim_software_context_switch(seq_len)
hard = sim_hardware_context_switch(seq_len)
speedup = soft / hard

print(f"Software Context Switch Latency: {soft:.2f} ms")
print(f"HW Context Switch Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
