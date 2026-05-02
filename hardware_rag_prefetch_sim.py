import math

def sim_software_rag_prefetch(chunks):
    # CPU interrupt + PCIe setup per RAG chunk
    return chunks * 1.5 

def sim_hardware_rag_prefetch(chunks):
    # Hardware async scatter-gather DMA queue
    return chunks * 0.05

chunks = 256
soft = sim_software_rag_prefetch(chunks)
hard = sim_hardware_rag_prefetch(chunks)
speedup = soft / hard

print(f"Software RAG Prefetch Latency: {soft:.2f} ms")
print(f"HW RAG Prefetch Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
