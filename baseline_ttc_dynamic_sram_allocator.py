import torch
import torch.nn as nn
import time

class TTCDynamicSRAMAllocator(nn.Module):
    """
    Test-Time Compute (TTC) Branching Divergence Hardware Simulator.
    Simulates dynamic SRAM allocation for multiple speculative branches.
    """
    def __init__(self, sram_capacity_mb=32, num_branches=4):
        super().__init__()
        self.sram_capacity = sram_capacity_mb * 1024 * 1024
        self.num_branches = num_branches
        self.active_branches = num_branches
        # Base allocation: equal split
        self.allocations = [self.sram_capacity // num_branches] * num_branches
        
    def forward(self, x, branch_probabilities):
        """
        x: input tensor [batch, seq, dim]
        branch_probabilities: tensor [num_branches] indicating confidence
        """
        # Reallocate SRAM dynamically based on branch probability (simulated Roofline adjustment)
        total_prob = torch.sum(branch_probabilities)
        for i in range(self.num_branches):
            self.allocations[i] = int(self.sram_capacity * (branch_probabilities[i].item() / total_prob.item()))
            
        # Simulate TTC compute divergence latency
        latency_cycles = 0
        for alloc in self.allocations:
            # If a branch gets too little SRAM, it spills to DRAM (high latency)
            if alloc < 2 * 1024 * 1024:  # Under 2MB threshold
                latency_cycles += 500  # DRAM spill penalty
            else:
                latency_cycles += 50   # In-SRAM hit
                
        return latency_cycles, self.allocations

if __name__ == "__main__":
    model = TTCDynamicSRAMAllocator()
    dummy_input = torch.randn(1, 128, 512)
    dummy_probs = torch.tensor([0.7, 0.1, 0.15, 0.05])
    latency, allocs = model(dummy_input, dummy_probs)
    print(f"Baseline TTC Dynamic SRAM Allocation Complete.")
    print(f"Simulated Latency Cycles: {latency}")
    print(f"Allocations (Bytes): {allocs}")
