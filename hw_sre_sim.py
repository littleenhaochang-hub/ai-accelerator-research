import time

def simulate_hw_sre():
    draft_length = 64
    batch_size = 16
    
    # Baseline: Software Speculative Rollback
    # On a miss, software must iterate through the KV cache page tables
    # and invalidate the tokens for the rejected draft steps across the batch.
    sw_invalidate_latency_per_token_us = 1.5 
    baseline_rollback_latency_us = draft_length * batch_size * sw_invalidate_latency_per_token_us
    baseline_rollback_latency_ms = baseline_rollback_latency_us / 1000.0
    
    # HW-SRE: Hardware Speculative Rollback Engine
    # Maintains a shadow pointer table in the NPU MMU. 
    # On a miss, a single "Restore" signal copies the shadow pointers back to active pointers in 1 cycle.
    hw_rollback_latency_cycles = 1
    npu_clock_freq_ghz = 2.0
    hw_rollback_latency_us = hw_rollback_latency_cycles / (npu_clock_freq_ghz * 1000)
    hw_rollback_latency_ms = hw_rollback_latency_us / 1000.0
    
    print("=== HW-SRE Simulation ===")
    print(f"Draft Length: {draft_length}, Batch Size: {batch_size}")
    print(f"Baseline Rollback Latency: {baseline_rollback_latency_ms:.4f} ms")
    print(f"HW-SRE Rollback Latency: {hw_rollback_latency_ms:.6f} ms")
    print(f"Speedup: {baseline_rollback_latency_ms/hw_rollback_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_sre()