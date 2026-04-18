import torch
import torch.nn as nn

class BaselineMoE(nn.Module):
    def __init__(self, num_experts, hidden_size):
        super().__init__()
        self.router = nn.Linear(hidden_size, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])

    def forward(self, x):
        # Late routing bottleneck
        routing_weights = torch.softmax(self.router(x), dim=-1)
        expert_idx = torch.argmax(routing_weights, dim=-1)
        
        # In hardware, fetching the chosen expert's weights here causes a massive HBM stall
        out = self.experts[expert_idx](x)
        return out
