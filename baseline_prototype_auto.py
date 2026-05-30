import torch
import torch.nn as nn

class BaselineMoEPrefetch(nn.Module):
    def __init__(self, num_experts=8, hidden_size=1024):
        super().__init__()
        self.num_experts = num_experts
        self.router = nn.Linear(hidden_size, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])

    def forward(self, x):
        # Baseline: No prefetching, just routing
        routing_logits = self.router(x)
        routing_weights = torch.softmax(routing_logits, dim=-1)
        top1_weight, top1_idx = torch.max(routing_weights, dim=-1)
        
        out = torch.zeros_like(x)
        for i in range(x.shape[0]):
            expert_idx = top1_idx[i].item()
            out[i] = self.experts[expert_idx](x[i]) * top1_weight[i]
        return out

if __name__ == "__main__":
    model = BaselineMoEPrefetch()
    x = torch.randn(16, 1024)
    out = model(x)
    print("Baseline MoE Prefetch pass completed. Output shape:", out.shape)
