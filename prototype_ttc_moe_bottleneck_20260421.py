import torch
import torch.nn as nn

class TTCMoEPrefetchBaseline(nn.Module):
    def __init__(self, hidden_dim=4096, num_experts=8, top_k=2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])

    def forward(self, x, test_time_compute_budget=1):
        # Bottleneck: Test-time compute routing introduces high latency in MoE expert prefetching.
        # This baseline mimics the stall cycles.
        route_scores = self.router(x)
        probs = torch.softmax(route_scores, dim=-1)
        top_probs, top_indices = torch.topk(probs, self.top_k, dim=-1)
        
        out = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = top_indices[0, i].item()
            # Simulate prefetch stall
            out += top_probs[0, i] * self.experts[expert_idx](x)
        return out

if __name__ == "__main__":
    print("Running TTC MoE Prefetch Baseline...")
    model = TTCMoEPrefetchBaseline()
    x = torch.randn(1, 4096)
    out = model(x)
    print("Completed forward pass with shape:", out.shape)
