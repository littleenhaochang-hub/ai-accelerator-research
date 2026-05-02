import math

def sim_software_router_sync(experts):
    return experts * 0.008 # CPU-GPU synchronization overhead for MoE routing

def sim_hardware_router_sync(experts):
    return experts * 0.00015 # Hardware async crossbar

experts = 2048
soft = sim_software_router_sync(experts)
hard = sim_hardware_router_sync(experts)
speedup = soft / hard

print(f"Software Router Sync Latency: {soft:.2f} ms")
print(f"HW Router Sync Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
