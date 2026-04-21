import torch
import torch.nn as nn

class TTCMoEBaseline(nn.Module):
    def __init__(self, hidden_dim=1024, num_experts=8):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])
        
    def forward(self, x):
        # Bottleneck: Test-time compute routing overhead and memory bandwidth
        gates = torch.softmax(self.router(x), dim=-1)
        top_k_gates, top_k_indices = torch.topk(gates, 2, dim=-1)
        out = torch.zeros_like(x)
        for i in range(x.shape[0]):
            for j in range(2):
                expert_idx = top_k_indices[i, j]
                out[i] += top_k_gates[i, j] * self.experts[expert_idx](x[i])
        return out

if __name__ == "__main__":
    model = TTCMoEBaseline()
    x = torch.randn(16, 1024)
    print("Forward pass complete:", model(x).shape)
