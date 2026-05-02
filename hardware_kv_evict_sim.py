import math

def sim_software_kv_evict(seq_len):
    return seq_len * 0.004 # Software maintaining LRU/MRU lists

def sim_hardware_kv_evict(seq_len):
    return seq_len * 0.0001 # Hardware ring buffer pointer update

seq_len = 131072 # 128K context
soft = sim_software_kv_evict(seq_len)
hard = sim_hardware_kv_evict(seq_len)
speedup = soft / hard

print(f"Software KV Eviction Latency: {soft:.2f} ms")
print(f"HW KV Eviction Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
