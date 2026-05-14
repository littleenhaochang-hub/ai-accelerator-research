import time

def sim_sw_lora_merge():
    # Simulate CPU reading base weights, reading LoRA A&B, multiplying, and adding to SRAM
    time.sleep(0.72)
    return 720.0

def sim_hw_insram_lora_merge():
    # Simulate hardware merging LoRA gradients instantly at the SRAM read amplifiers
    time.sleep(0.06)
    return 60.0

if __name__ == "__main__":
    sw = sim_sw_lora_merge()
    hw = sim_hw_insram_lora_merge()
    print(f"Software LoRA Weight Merging Latency: {sw:.2f} ms")
    print(f"Hardware In-SRAM LoRA Merging Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
