import time

def simulate_hw_cele():
    vocab_size = 128000
    batch_size = 1
    seq_len = 2048 # Local fine-tuning / Test-time training
    
    # Baseline: Materialize logits to SRAM, compute Softmax, compute CE Loss, then compute grad
    # logits size: 2048 * 128000 * 2 bytes = 512 MB
    logits_size_mb = (seq_len * vocab_size * 2) / (1024 * 1024)
    sram_bw_gbps = 2000
    
    # Baseline involves writing logits, reading them for softmax/loss, and writing gradients
    baseline_sram_traffic_mb = logits_size_mb * 3 
    # Approximation of memory-bound latency + kernel overheads
    baseline_latency_ms = (baseline_sram_traffic_mb / 1024) / sram_bw_gbps * 1000 * 2.0
    
    # HW-CELE (Hardware Cross-Entropy Loss Engine):
    # Fuses the final Linear layer projection, Softmax, and Cross Entropy loss into a single inline engine.
    # We only write the final gradient back to SRAM, dropping intermediate logits traffic.
    fuser_sram_traffic_mb = logits_size_mb * 1 
    fuser_latency_ms = (fuser_sram_traffic_mb / 1024) / sram_bw_gbps * 1000 * 1.2
    
    print("=== HW-CELE Simulation ===")
    print(f"Vocab Size: {vocab_size}, Sequence Length: {seq_len}")
    print(f"Baseline SRAM Traffic: {baseline_sram_traffic_mb:.2f} MB")
    print(f"HW-CELE SRAM Traffic: {fuser_sram_traffic_mb:.2f} MB")
    print(f"Baseline Latency: {baseline_latency_ms:.4f} ms")
    print(f"HW-CELE Latency: {fuser_latency_ms:.4f} ms")
    print(f"Speedup: {baseline_latency_ms/fuser_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_cele()
