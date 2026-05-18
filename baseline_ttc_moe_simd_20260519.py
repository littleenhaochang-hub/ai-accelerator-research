import torch
import torch.nn as nn
import time

class TTCMoEBaseline(nn.Module):
    def __init__(self, d_model=512, num_experts=8, top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts)
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])
        
    def forward(self, x):
        # TTC Phase: Branching Divergence Check
        route_logits = self.router(x)
        probs = torch.softmax(route_logits, dim=-1)
        top_probs, top_indices = torch.topk(probs, self.top_k, dim=-1)
        
        out = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = top_indices[:, i]
            # SIMD Divergence simulated by sequential bottleneck
            for batch_idx, e_idx in enumerate(expert_idx):
                out[batch_idx] += top_probs[batch_idx, i] * self.experts[e_idx](x[batch_idx])
        return out

if __name__ == "__main__":
    model = TTCMoEBaseline()
    x = torch.randn(128, 512)
    start = time.time()
    y = model(x)
    print(f"Baseline TTC MoE latency: {(time.time()-start)*1000:.2f} ms")
