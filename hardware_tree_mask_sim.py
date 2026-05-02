import math

def sim_software_tree_mask(draft_tokens):
    return draft_tokens * 0.05 # Software building tree mask arrays

def sim_hardware_tree_mask(draft_tokens):
    return draft_tokens * 0.001 # Hardware inline tree mask generator

draft_tokens = 256
soft = sim_software_tree_mask(draft_tokens)
hard = sim_hardware_tree_mask(draft_tokens)
speedup = soft / hard

print(f"Software Tree Mask Latency: {soft:.2f} ms")
print(f"HW Tree Mask Latency: {hard:.2f} ms")
print(f"Speedup: {speedup:.2f}x")
