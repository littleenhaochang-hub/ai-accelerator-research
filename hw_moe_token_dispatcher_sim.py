import numpy as np

def simulate_hw_moe_token_dispatcher(batch_size, seq_len, num_experts, hidden_dim):
    print(f"Simulating Hardware MoE Token Dispatcher (HW-MTD) - Tokens: {batch_size*seq_len}, Experts: {num_experts}")
    
    total_tokens = batch_size * seq_len
    
    # Software Scatter/Gather (Memory bound with random accesses)
    # Read tokens, compute indices, write to scattered buffers, read back
    sw_latency_per_token = (hidden_dim * 2) / (50e9) * 1000 + 0.005 # 50GB/s random access + overhead
    sw_total_latency = total_tokens * sw_latency_per_token
    
    # Hardware Token Dispatcher (Inline Crossbar routing)
    # Tokens flow directly into contiguous expert FIFO queues
    hw_latency_per_token = (hidden_dim * 2) / (800e9) * 1000 # 800GB/s contiguous SRAM bandwidth
    hw_total_latency = total_tokens * hw_latency_per_token
    
    print(f"Software Scatter/Gather Latency: {sw_total_latency:.4f} ms")
    print(f"Hardware Dispatcher Latency: {hw_total_latency:.4f} ms")
    print(f"Latency Reduction: {(sw_total_latency - hw_total_latency) / sw_total_latency * 100:.2f}%")
    print(f"Speedup: {sw_total_latency / hw_total_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_moe_token_dispatcher(32, 2048, 64, 4096)
