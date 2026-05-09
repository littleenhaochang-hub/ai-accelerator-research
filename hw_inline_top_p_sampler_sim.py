import numpy as np

def simulate_hardware_top_p_sampler(vocab_size):
    print(f"Simulating Hardware Inline Top-P Sampler Engine (HW-ITPSE) - Vocab: {vocab_size}")
    
    # Software Sampling (PCIe Transfer + CPU Sort + CPU Sample)
    pcie_latency = (vocab_size * 2) / (16e9) * 1000  # 16 GB/s PCIe Gen4
    cpu_sort_latency = vocab_size * np.log2(vocab_size) * 1e-6  # O(N log N) approximation
    sw_latency = pcie_latency + cpu_sort_latency
    
    # Hardware Inline Sampling (NPU SRAM Comparator Tree)
    # Fully parallel execution in O(1) clock cycles
    hw_latency = 0.005  # 5 microseconds hardware delay
    
    print(f"Software CPU Sampling Latency: {sw_latency:.4f} ms")
    print(f"Hardware Inline Sampling Latency: {hw_latency:.4f} ms")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hardware_top_p_sampler(128256)
