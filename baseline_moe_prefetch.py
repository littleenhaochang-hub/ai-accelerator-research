import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, num_experts=8, hidden_size=4096):
        super().__init__()
        self.num_experts = num_experts
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])
        self.router = nn.Linear(hidden_size, num_experts)
        
    def forward(self, x):
        # Bottleneck: Routing probabilities computed late, causing memory stall for expert weights
        route_probs = torch.softmax(self.router(x), dim=-1)
        top_expert = torch.argmax(route_probs, dim=-1)
        # Sequential execution limits bandwidth utilization
        return self.experts[top_expert](x)

if __name__ == "__main__":
    model = MoEPrefetchBaseline()
    x = torch.randn(1, 4096)
    out = model(x)
    print("Baseline MoE executed. Roofline analysis: memory-bound due to late weight fetch.")
