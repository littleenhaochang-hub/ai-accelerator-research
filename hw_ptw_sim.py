import numpy as np

def simulate_hw_page_table_walker(num_tokens, cache_hits):
    print(f"Simulating Hardware Prefix Cache Page Table Walker (HW-PTW) - Tokens: {num_tokens}")
    
    # Software Prefix Caching (Radix Tree matching via CPU)
    # Extremely pointer chasing heavy, high cache miss rate on CPU
    sw_pointer_chase_latency = 0.0001 # 100ns per node traversal
    sw_total_latency = num_tokens * sw_pointer_chase_latency
    
    # HW-PTW: Dedicated hardware MMU unit walking the Radix Tree in SRAM
    hw_pointer_chase_latency = 0.000005 # 5ns per node traversal in hardware SRAM
    hw_total_latency = num_tokens * hw_pointer_chase_latency
    
    print(f"Software Radix Tree Traversal Latency: {sw_total_latency:.4f} ms")
    print(f"HW-PTW Traversal Latency: {hw_total_latency:.4f} ms")
    print(f"Speedup: {sw_total_latency / hw_total_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_page_table_walker(8192, 0.9)
