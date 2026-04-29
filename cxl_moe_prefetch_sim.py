import torch
import torch.nn as nn
import time

class CXLMoEPrefetchSim:
    def __init__(self, num_experts=16, expert_size_mb=100, pcie_bw_gbps=64, cxl_bw_gbps=128):
        self.num_experts = num_experts
        self.expert_size_mb = expert_size_mb
        self.pcie_bw_gbps = pcie_bw_gbps
        self.cxl_bw_gbps = cxl_bw_gbps
        self.compute_time_per_expert_ms = 2.0
        
    def simulate_demand_loading(self, num_tokens=100):
        total_time_ms = 0
        transfer_time_ms = (self.expert_size_mb / (self.pcie_bw_gbps * 1024)) * 1000
        for _ in range(num_tokens):
            # Demand load blocks compute
            total_time_ms += transfer_time_ms + self.compute_time_per_expert_ms
        return total_time_ms
        
    def simulate_cxl_prefetching(self, num_tokens=100, prediction_accuracy=0.9):
        total_time_ms = 0
        transfer_time_ms = (self.expert_size_mb / (self.cxl_bw_gbps * 1024)) * 1000
        for _ in range(num_tokens):
            if torch.rand(1).item() < prediction_accuracy:
                # Correct prediction: transfer is hidden behind compute
                total_time_ms += max(transfer_time_ms, self.compute_time_per_expert_ms)
            else:
                # Mispredict: wait for transfer
                total_time_ms += transfer_time_ms + self.compute_time_per_expert_ms
        return total_time_ms

if __name__ == "__main__":
    sim = CXLMoEPrefetchSim()
    demand_time = sim.simulate_demand_loading(1000)
    cxl_time = sim.simulate_cxl_prefetching(1000, 0.9)
    print(f"Demand Loading Latency: {demand_time:.2f} ms")
    print(f"CXL Prefetching Latency: {cxl_time:.2f} ms")
    print(f"Speedup: {demand_time / cxl_time:.2f}x")
