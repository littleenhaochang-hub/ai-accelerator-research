import math

def sim_standard_kv(seq_len):
    # 50us per token fetch from DRAM
    return seq_len * 0.05

def sim_skcb(seq_len, hit_rate):
    # 1us for SRAM hit, 50us for DRAM miss
    sram_time = seq_len * hit_rate * 0.001
    dram_time = seq_len * (1 - hit_rate) * 0.05
    return sram_time + dram_time

seq_len = 8192
hit_rate = 0.45

std_latency = sim_standard_kv(seq_len)
skcb_latency = sim_skcb(seq_len, hit_rate)
speedup = std_latency / skcb_latency

print(f"Standard KV Fetch Latency: {std_latency:.2f} ms")
print(f"SKCB Latency: {skcb_latency:.2f} ms")
print(f"Throughput Speedup: {speedup:.2f}x")
