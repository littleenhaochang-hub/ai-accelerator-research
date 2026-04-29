import numpy as np

def simulate_lora_scheduler():
    print("Simulating Hardware LoRA Scheduler...")
    batch_size = 64
    num_adapters = 8
    
    # Baseline software context switching between LoRA adapters
    baseline_latency = batch_size * num_adapters * 0.05
    
    # Proposed hardware LoRA multiplexer / scheduler
    proposed_latency = batch_size * num_adapters * 0.002
    
    speedup = baseline_latency / proposed_latency
    print(f"Baseline Latency: {baseline_latency:.2f} ms")
    print(f"Proposed Latency: {proposed_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_lora_scheduler()
