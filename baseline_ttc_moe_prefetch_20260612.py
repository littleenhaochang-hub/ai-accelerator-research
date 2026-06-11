import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, hidden_dim, num_experts, top_k):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])
        self.top_k = top_k

    def forward(self, x):
        # Bottleneck: Test-time compute routing divergence and SRAM bandwidth
        logits = self.router(x)
        probs = torch.softmax(logits, dim=-1)
        top_probs, top_indices = torch.topk(probs, self.top_k)
        
        out = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = top_indices[:, i]
            # In hardware, this causes random SRAM reads
            for b in range(x.size(0)):
                out[b] += top_probs[b, i] * self.experts[expert_idx[b]](x[b:b+1]).squeeze(0)
        return out

if __name__ == "__main__":
    model = MoEPrefetchBaseline(128, 8, 2)
    x = torch.randn(4, 128)
    y = model(x)
    print("Baseline execution complete. Bottleneck identified: Random SRAM reads during expert selection.")
