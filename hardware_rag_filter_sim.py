import math

def sim_software_rag_filter(context_len):
    return context_len * 0.008 # similarity scores via software

def sim_hardware_rag_filter(context_len):
    return context_len * 0.0002 # inline hardware matching

context_len = 131072 # 128K tokens
soft = sim_software_rag_filter(context_len)
hard = sim_hardware_rag_filter(context_len)
speedup = soft / hard

print(f"Software RAG Filter Latency: {soft:.2f} ms")
print(f"HW RAG Filter Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
