import time

def simulate_hw_sdeee(draft_layers=8, early_exit_layer=3):
    # Baseline: Software Early-Exit for Speculative Draft Models
    # Needs memory read/write for confidence check at intermediate layers
    software_latency_ms = draft_layers * 0.1 + early_exit_layer * 0.05 
    
    # Proposed: Hardware Speculative Draft Early-Exit Engine (HW-SDEEE)
    # Inline confidence check at MAC output, stops clock for remaining layers instantly
    hardware_latency_ms = early_exit_layer * 0.1 + 0.002
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Draft Layers: {draft_layers}, Average Exit Layer: {early_exit_layer}")
    print(f"Baseline Latency (Software Check): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-SDEEE): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_sdeee()
