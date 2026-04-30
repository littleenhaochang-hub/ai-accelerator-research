import math

def sim_software_expert_pruning(experts):
    return experts * 0.005 # Software sorting and pruning threshold

def sim_hardware_expert_pruning(experts):
    return experts * 0.0001 # Hardware inline comparator

experts = 8192
soft = sim_software_expert_pruning(experts)
hard = sim_hardware_expert_pruning(experts)
speedup = soft / hard

print(f"Software Expert Pruning Latency: {soft:.2f} ms")
print(f"HW Expert Pruning Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
