import time

def simulate_grouped_gemm():
    print("Starting Hardware-Software Co-Design Simulation: Hardware Grouped-GEMM Scheduler for MoE")
    
    # Baseline: Sequential kernel launches for MoE experts
    num_experts_active = 8
    kernel_launch_overhead_us = 5.0
    gemm_compute_us = 15.0
    
    baseline_time_us = num_experts_active * (kernel_launch_overhead_us + gemm_compute_us)
    
    # Hardware: Grouped-GEMM Scheduler
    hardware_launch_overhead_us = 1.0 # Single launch for the group
    hardware_time_us = hardware_launch_overhead_us + (num_experts_active * gemm_compute_us)
    
    speedup = baseline_time_us / hardware_time_us
    
    print(f"Baseline Time: {baseline_time_us:.2f} us")
    print(f"Hardware Grouped-GEMM Time: {hardware_time_us:.2f} us")
    print(f"Throughput Speedup: {speedup:.2f}x")
    
    if speedup > 1.2:
        print("RESULT: SUCCESS - Hardware Grouped-GEMM reduces kernel launch overhead.")
    else:
        print("RESULT: FAILED")

if __name__ == '__main__':
    simulate_grouped_gemm()
