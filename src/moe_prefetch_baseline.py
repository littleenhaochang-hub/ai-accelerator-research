import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, d_model=512, num_experts=8, top_k=2):
        super().__init__()
        self.router = nn.Linear(d_model, num_experts)
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])
        self.top_k = top_k

    def forward(self, x):
        # Hardware Bottleneck: Router latency blocking expert SRAM loading
        logits = self.router(x)
        probs, indices = torch.topk(logits, self.top_k, dim=-1)
        
        # Simulated Prefetch delay bottleneck here
        out = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = indices[:, i]
            # In a real HW simulator, this is where SRAM prefetching stalls occur
            for batch_idx, e_idx in enumerate(expert_idx):
                out[batch_idx] += probs[batch_idx, i] * self.experts[e_idx](x[batch_idx])
                
        return out

if __name__ == "__main__":
    model = MoEPrefetchBaseline()
    dummy_input = torch.randn(16, 512)
    print("Baseline MoE Prefetch pass complete. Output shape:", model(dummy_input).shape)
