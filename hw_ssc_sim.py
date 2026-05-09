import numpy as np

def simulate_hw_ssm_state_compressor(seq_len, dim, state_dim):
    print(f"Simulating Hardware SSM State Compressor (HW-SSC) - Seq: {seq_len}, Dim: {dim}, State Dim: {state_dim}")
    
    # Standard Mamba/SSM State (Dense FP16)
    fp16_mem = seq_len * state_dim * dim * 2
    
    # HW-SSC: Factorize state dynamically using an inline low-rank projector
    # Stores rank-8 representations instead of full state_dim (e.g., 128)
    rank = 8
    sparse_mem = (seq_len * rank * dim * 2) + (rank * state_dim * 2) # Core tensor + projection matrices
    
    print(f"Dense FP16 State Memory: {fp16_mem/1e9:.2f} GB")
    print(f"HW-SSC Compressed Memory: {sparse_mem/1e9:.2f} GB")
    print(f"Memory Reduction: {(fp16_mem - sparse_mem) / fp16_mem * 100:.2f}%")

if __name__ == "__main__":
    # Huge context simulation (e.g., 1M tokens)
    simulate_hw_ssm_state_compressor(1048576, 1024, 128)
