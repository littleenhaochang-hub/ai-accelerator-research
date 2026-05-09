import time

def simulate_hw_asfd():
    seq_len = 1024
    
    # Baseline: CPU schedules draft model execution, then target model
    # CPU overhead for coordinating draft and target models
    cpu_scheduling_latency_ms = 0.5 
    draft_compute_ms = 1.2
    target_compute_ms = 4.0
    
    # In software, the draft model tokens must be passed back to CPU, evaluated, and then sent to target model
    baseline_latency_ms = (cpu_scheduling_latency_ms + draft_compute_ms + cpu_scheduling_latency_ms + target_compute_ms) * (seq_len / 4) # Assuming 4 tokens per draft
    
    # HW-ASFD: Hardware Asynchronous Speculative Fetching Engine
    # Draft model and Target model run concurrently on different NPU chiplets or partitions.
    # HW synchronizes the tokens.
    hw_sync_latency_ms = 0.05
    # Target compute overlaps with next draft compute
    hw_latency_ms = (hw_sync_latency_ms + max(draft_compute_ms, target_compute_ms)) * (seq_len / 4)
    
    print("=== HW-ASFD Simulation ===")
    print(f"Sequence Length: {seq_len}")
    print(f"Baseline Latency (Software Speculative Scheduling): {baseline_latency_ms:.2f} ms")
    print(f"HW-ASFD Latency (Hardware Async Fetching): {hw_latency_ms:.2f} ms")
    print(f"Speedup: {baseline_latency_ms/hw_latency_ms:.2f}x")

if __name__ == '__main__':
    simulate_hw_asfd()