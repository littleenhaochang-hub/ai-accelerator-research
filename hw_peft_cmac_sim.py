import time

def simulate_hw_peft_cmac(batch_size=128, lora_adapters=64):
    # Baseline: Software multi-tenant LoRA batching (memory-bound fetching of different adapters)
    software_latency_ms = (batch_size * lora_adapters) * 0.005 
    
    # Proposed: Hardware PEFT Context-MAC (HW-PEFT-CMAC)
    # Uses dedicated SRAM to pin LoRA adapters and a hardware context-switcher for the MAC arrays
    hardware_latency_ms = (batch_size * lora_adapters) * 0.0001
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Batch Size: {batch_size}, Active LoRA Adapters: {lora_adapters}")
    print(f"Baseline Latency (Software Multi-Tenant): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-PEFT-CMAC): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_peft_cmac()
