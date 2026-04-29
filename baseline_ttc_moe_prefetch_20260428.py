import torch
import torch.nn as nn
import time

class TTC_MoE_Prefetch_Baseline(nn.Module):
    def __init__(self, d_model=4096, num_experts=8, top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts)
        # Mock experts
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])
        
    def forward(self, x):
        # x: (batch_size, seq_len, d_model)
        routing_logits = self.router(x)
        routing_probs = torch.softmax(routing_logits, dim=-1)
        topk_probs, topk_indices = torch.topk(routing_probs, self.top_k, dim=-1)
        
        out = torch.zeros_like(x)
        for i in range(self.num_experts):
            mask = (topk_indices == i).any(dim=-1)
            if mask.any():
                # Bottleneck: Memory fetch for expert weights happens here sequentially
                expert_out = self.experts[i](x[mask])
                out[mask] += expert_out
        return out

if __name__ == "__main__":
    model = TTC_MoE_Prefetch_Baseline()
    x = torch.randn(2, 1024, 4096)
    start = time.time()
    out = model(x)
    end = time.time()
    print(f"Latency: {(end-start)*1000:.2f} ms")
    print("Baseline execution complete. Ready for Auto-Researcher optimization.")