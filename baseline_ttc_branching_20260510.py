import torch
import torch.nn as nn

class TTCBranchingMoE(nn.Module):
    def __init__(self, hidden_size=512, num_experts=4):
        super().__init__()
        self.router = nn.Linear(hidden_size, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])
        
    def forward(self, x):
        # Simplistic Test-Time Compute branching
        routing_weights = torch.softmax(self.router(x), dim=-1)
        out = torch.zeros_like(x)
        for i, expert in enumerate(self.experts):
            out += routing_weights[:, i:i+1] * expert(x)
        return out

if __name__ == "__main__":
    model = TTCBranchingMoE()
    x = torch.randn(16, 512)
    print("Baseline TTC-MoE initialized. Output shape:", model(x).shape)
