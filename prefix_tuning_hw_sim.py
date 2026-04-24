import time

def software_prefix_tuning(batch_size, prefix_len, d_model):
    # Simulated latency for Software Prefix Tuning
    # CPU/GPU must concatenate the soft-prompt tensors to every request's input
    # Requires large matrix copies and memory fragmentation
    latency = batch_size * prefix_len * d_model * 0.0001
    return latency

def hardware_prefix_tuning(batch_size, prefix_len, d_model):
    # Simulated latency for Hardware Prefix Tuning Engine
    # Shared prefix resides in SRAM permanently. 
    # Hardware MMU zero-copy broadcasts it to the MAC arrays.
    latency = batch_size * prefix_len * d_model * 0.000005
    return latency

def main():
    batch_size = 256
    prefix_len = 1024  # Continuous soft-prompt length
    d_model = 4096
    
    print("Running Hardware Prefix Tuning Injection Simulation...")
    sw_lat = software_prefix_tuning(batch_size, prefix_len, d_model)
    print(f"Software Prefix Injection Latency: {sw_lat:.2f} ms")
    
    hw_lat = hardware_prefix_tuning(batch_size, prefix_len, d_model)
    print(f"Hardware Prefix Injection Latency: {hw_lat:.2f} ms")
    
    speedup = sw_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
