import torch
import torch.nn as nn

class TTC_MoE_Prefetch_Baseline(nn.Module):
    def __init__(self, hidden_dim, num_experts):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])
        
    def forward(self, x):
        # TTC step: routing probability
        route_logits = self.router(x)
        topk_vals, topk_indices = torch.topk(route_logits, 2, dim=-1)
        
        # Bottleneck: expert weights must be fetched from memory here
        out = torch.zeros_like(x)
        for i, idx in enumerate(topk_indices[0]):
            out += self.experts[idx](x) * topk_vals[0][i]
        return out

if __name__ == "__main__":
    model = TTC_MoE_Prefetch_Baseline(128, 8)
    dummy_input = torch.randn(1, 128)
    print("Output shape:", model(dummy_input).shape)
