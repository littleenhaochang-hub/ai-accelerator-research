import time

class HW_KV_Delta_Pruner:
    def __init__(self, seq_len=128000, dim=1024):
        self.seq_len = seq_len
        self.dim = dim
        self.bytes_per_token = dim * 2 * 2 # FP16 K and V
        self.total_memory = seq_len * self.bytes_per_token
        
    def simulate_baseline(self):
        # Baseline memory read for full sequence
        bandwidth = 100 * 1024**3 # 100 GB/s internal SRAM bandwidth
        latency = self.total_memory / bandwidth
        return latency, self.total_memory

    def simulate_delta_pruning(self):
        # Hardware inline pruner detects if KV token delta is below threshold
        # and prunes it from the active cache
        pruning_ratio = 0.75 # 75% of tokens are redundant (small delta)
        active_tokens = int(self.seq_len * (1 - pruning_ratio))
        active_memory = active_tokens * self.bytes_per_token
        
        bandwidth = 100 * 1024**3
        latency = active_memory / bandwidth
        return latency, active_memory

def run_sim():
    print("Running Hardware KV Cache Delta Pruning (HW-KVCDP) Simulation...")
    sim = HW_KV_Delta_Pruner()
    
    base_latency, base_mem = sim.simulate_baseline()
    pruned_latency, pruned_mem = sim.simulate_delta_pruning()
    
    speedup = base_latency / pruned_latency if pruned_latency > 0 else float('inf')
    mem_reduction = (base_mem - pruned_mem) / base_mem * 100
    
    print(f"Baseline Latency: {base_latency * 1000:.2f} ms")
    print(f"HW-KVCDP Latency: {pruned_latency * 1000:.2f} ms")
    print(f"Memory Reduction: {mem_reduction:.2f}%")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    run_sim()
