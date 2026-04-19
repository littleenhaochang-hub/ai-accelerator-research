import math

def simulate_diff_transformer():
    # Differential Attention computes:
    # Attn = Softmax(Q1 * K1 / sqrt(d)) - Softmax(Q2 * K2 / sqrt(d))
    seq_len = 4096
    head_dim = 64 # split 128 into 2x64
    num_heads = 32
    
    # Standard Attention MACs
    # Q * K^T = N^2 * D
    standard_macs = seq_len * seq_len * (head_dim * 2) * num_heads
    
    # Diff Attention MACs
    # Two parallel Q*K^T with half dim
    diff_macs_1 = seq_len * seq_len * head_dim * num_heads
    diff_macs_2 = seq_len * seq_len * head_dim * num_heads
    total_diff_macs = diff_macs_1 + diff_macs_2
    
    # Hardware Overhead: Vector Subtraction after Softmax
    subtraction_ops = seq_len * seq_len * num_heads
    
    print("--- Differential Transformer Hardware Simulation ---")
    print(f"Standard Attention MACs: {standard_macs:.2e}")
    print(f"Diff Attention MACs: {total_diff_macs:.2e}")
    print(f"Compute Ratio: {total_diff_macs / standard_macs:.2f}x")
    print(f"Vector Subtractions (Overhead): {subtraction_ops:.2e} ops")
    print("Conclusion: Diff Transformer splits the head dimension in half, keeping total MACs identical. The only overhead is the final element-wise subtraction. Hardware should integrate a 'Differential Softmax ALU' to fuse the subtraction and avoid writing two attention maps to SRAM.")

if __name__ == "__main__":
    simulate_diff_transformer()
