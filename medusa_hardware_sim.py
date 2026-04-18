import math

def simulate_medusa_hardware():
    # Medusa speculative decoding appends K heads to predict K future tokens simultaneously.
    # Typical K=4. Hidden dim = 4096.
    
    K = 4
    hidden_dim = 4096
    vocab_size = 32000
    
    # Standard decoding: 1 token/step. Read full weights (e.g. 7B = 3.5GB in INT4)
    model_size_gb = 3.5
    memory_bw_gbps = 100.0 # LPDDR5
    
    standard_latency_ms = (model_size_gb / memory_bw_gbps) * 1000
    
    # Medusa overhead
    # Each Medusa head is a small ResNet block + Linear projection to vocab
    # roughly: 1 layer of hidden_dim x hidden_dim + hidden_dim x vocab_size
    medusa_head_params = (hidden_dim * hidden_dim) + (hidden_dim * vocab_size)
    medusa_total_params = medusa_head_params * K
    medusa_total_gb = (medusa_total_params * 2) / (1024**3) # FP16 overhead
    
    medusa_step_latency_ms = ((model_size_gb + medusa_total_gb) / memory_bw_gbps) * 1000
    
    # Assuming acceptance rate of 2.5 tokens per step
    acceptance_rate = 2.5
    
    medusa_tps = acceptance_rate / (medusa_step_latency_ms / 1000)
    standard_tps = 1.0 / (standard_latency_ms / 1000)
    
    speedup = medusa_tps / standard_tps
    
    print("--- Medusa Speculative Decoding Hardware Simulation ---")
    print(f"Medusa Heads Memory Overhead: {medusa_total_gb*1024:.2f} MB")
    print(f"Standard TPS: {standard_tps:.2f}")
    print(f"Medusa TPS: {medusa_tps:.2f}")
    print(f"Effective Speedup: {speedup:.2f}x")
    print("Conclusion: Medusa significantly boosts TPS but introduces a large memory footprint for the heads (often 1GB+ in FP16). Hardware must support parallel tree-mask verification for the generated candidates.")

if __name__ == "__main__":
    simulate_medusa_hardware()
