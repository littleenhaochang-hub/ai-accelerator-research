import time

def simulate_software_backprop(seq_len, hidden_dim):
    # Standard backpropagation: Forward pass, backward pass, weight update
    # Requires storing massive activation checkpoints in DRAM
    latency = (seq_len * hidden_dim * 3) / 1e10 
    memory_overhead = 0.05 # 50ms memory bottleneck
    return latency + memory_overhead

def simulate_hw_forward_gradient(seq_len, hidden_dim):
    # Hardware Continuous Test-Time Training: Forward-gradient method
    # Updates weights inline during the forward pass, zero activation memory
    latency = (seq_len * hidden_dim * 1.1) / 1e10 
    return latency

if __name__ == "__main__":
    seq_len = 4096
    hidden_dim = 4096
    
    soft_time = simulate_software_backprop(seq_len, hidden_dim)
    hw_time = simulate_hw_forward_gradient(seq_len, hidden_dim)
    
    print(f"Software Backprop Latency: {soft_time:.4f} s")
    print(f"HW-CTTT Latency: {hw_time:.4f} s")
    print(f"Speedup: {soft_time / hw_time:.2f}x")
