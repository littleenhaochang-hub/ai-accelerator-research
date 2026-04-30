import math

def sim_linear(seq_len):
    return seq_len * 0.05

def sim_nlq(seq_len):
    return seq_len * 0.0125 + seq_len * 0.005

seq_len = 16384
lin = sim_linear(seq_len)
nlq = sim_nlq(seq_len)
speedup = lin / nlq

print(f"Linear Fetch Latency: {lin:.2f} ms")
print(f"NLQ Fetch + Decode Latency: {nlq:.2f} ms")
print(f"Throughput Speedup: {speedup:.2f}x")
