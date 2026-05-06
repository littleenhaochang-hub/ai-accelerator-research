import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, d_model=4096, num_experts=8):
        super().__init__()
        self.router = nn.Linear(d_model, num_experts)
        # Mock experts in HBM
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])
        
    def forward(self, x):
        # Bottleneck: Routing happens here, meaning expert weights must be fetched synchronously.
        routing_logits = self.router(x)
        expert_idx = torch.argmax(routing_logits, dim=-1)
        
        # Pipeline stalls waiting for HBM to SRAM transfer of expert_idx weights
        return self.experts[expert_idx](x)
