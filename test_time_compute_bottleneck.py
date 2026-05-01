import torch
import torch.nn as nn

class TTCBottleneckSim(nn.Module):
    def __init__(self, hidden_dim=4096, branches=4):
        super().__init__()
        self.branches = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(branches)])
        self.router = nn.Linear(hidden_dim, branches)
        
    def forward(self, x):
        # Bottleneck: SRAM spilling during parallel branch evaluation for Test-Time Compute
        scores = torch.softmax(self.router(x), dim=-1)
        out = sum(score.unsqueeze(-1) * branch(x) for score, branch in zip(scores.unbind(-1), self.branches))
        return out

if __name__ == '__main__':
    model = TTCBottleneckSim()
    x = torch.randn(1, 4096)
    print("Baseline TTC pass:", model(x).shape)
