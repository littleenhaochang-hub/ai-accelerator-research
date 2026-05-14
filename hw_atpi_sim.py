import time

def simulate_software_tensor_parallelism(seq_len, hidden_dim):
    # CPU orchestrated All-Reduce across chiplets over PCIe
    compute_time = (seq_len * hidden_dim) / 1e10
    sync_overhead = 0.008 # 8ms PCIe + CPU driver sync
    return compute_time + sync_overhead

def simulate_hardware_atpi(seq_len, hidden_dim):
    # Hardware Asynchronous Tensor-Parallel Interconnect (Zero CPU sync)
    compute_time = (seq_len * hidden_dim) / 1e10
    hw_sync = 0.0001 # 100us pure hardware link
    return compute_time + hw_sync

if __name__ == "__main__":
    seq_len = 8192
    hidden_dim = 4096
    
    soft_time = simulate_software_tensor_parallelism(seq_len, hidden_dim)
    hw_time = simulate_hardware_atpi(seq_len, hidden_dim)
    
    print(f"Software All-Reduce Latency: {soft_time:.4f} s")
    print(f"HW-ATPI Interconnect Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
