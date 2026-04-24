import torch
import torch.nn as nn

class TTCMoEPrefetchBaseline(nn.Module):
    def __init__(self, d_model=1024, num_experts=8, top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts)
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])

    def forward(self, x):
        # TTC Branching - Dynamic routing causes memory stall bottlenecks
        router_logits = self.router(x)
        routing_weights = torch.softmax(router_logits, dim=-1)
        top_weights, top_indices = torch.topk(routing_weights, self.top_k, dim=-1)
        
        out = torch.zeros_like(x)
        # Prefetching simulation bottleneck
        for i in range(self.top_k):
            expert_idx = top_indices[:, i]
            # Simulated stall: dynamic expert load
            for b in range(x.size(0)):
                out[b] += top_weights[b, i] * self.experts[expert_idx[b]](x[b:b+1]).squeeze(0)
        return out

if __name__ == "__main__":
    model = TTCMoEPrefetchBaseline()
    x = torch.randn(4, 1024)
    print("Running baseline TTC MoE prefetch bottleneck prototype...")
    out = model(x)
    print("Output shape:", out.shape)
