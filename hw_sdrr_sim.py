import numpy as np

def simulate_hw_spec_draft_rejection_recycler(draft_len, dim):
    print(f"Simulating Hardware Speculative Draft Rejection Recycler (HW-SDRR) - Draft Tokens: {draft_len}, Dim: {dim}")
    
    # Software Rollback + Recompute
    # Re-computing rejected tokens costs full MAC latency
    sw_recompute_macs = draft_len * dim * dim * 4
    sw_latency = sw_recompute_macs / (100e12) * 1000 + 0.5 # 0.5ms state rollback overhead
    
    # HW-SDRR: Rejected states are kept in a speculative shadow buffer. 
    # If the target model eventually matches a rejected path (common in beam/tree searches),
    # the hardware instantly restores the state from the shadow buffer without MAC recomputation.
    # Assuming a 60% eventual hit rate for previously rejected sub-trees.
    hit_rate = 0.60
    hw_recompute_macs = draft_len * dim * dim * 4 * (1 - hit_rate)
    hw_latency = hw_recompute_macs / (100e12) * 1000 + 0.005 # 5us shadow buffer restore
    
    print(f"Software Rollback & Recompute Latency: {sw_latency:.4f} ms")
    print(f"HW-SDRR Latency: {hw_latency:.4f} ms")
    print(f"Speedup: {sw_latency / hw_latency:.2f}x")

if __name__ == "__main__":
    simulate_hw_spec_draft_rejection_recycler(64, 4096)
