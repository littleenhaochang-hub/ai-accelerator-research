import torch
import torch.nn as nn

class TTCBottleneckPrototype(nn.Module):
    def __init__(self, hidden_dim=1024, num_experts=8):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts)
        # Mock experts
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])

    def forward(self, x):
        routing_weights = torch.softmax(self.router(x), dim=-1)
        # Bottleneck: Dynamic routing causes SRAM latency
        out = sum(routing_weights[:, i:i+1] * self.experts[i](x) for i in range(len(self.experts)))
        return out

if __name__ == "__main__":
    model = TTCBottleneckPrototype()
    dummy_input = torch.randn(32, 1024)
    print("Running prototype forward pass...")
    model(dummy_input)
    print("Done.")
