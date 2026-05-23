import torch
import torch.nn as nn

class BaselineMoEPrefetch(nn.Module):
    def __init__(self, hidden_dim=512, num_experts=8, top_k=2):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])
        self.top_k = top_k
        self.prefetch_buffer = {}

    def forward(self, x):
        routing_logits = self.router(x)
        routing_probs = torch.softmax(routing_logits, dim=-1)
        topk_probs, topk_indices = torch.topk(routing_probs, self.top_k, dim=-1)
        
        # Simulate prefetch bottleneck
        for idx in topk_indices.view(-1).unique():
            if idx.item() not in self.prefetch_buffer:
                self.prefetch_buffer[idx.item()] = self.experts[idx.item()]
                
        out = torch.zeros_like(x)
        for b in range(x.size(0)):
            for i in range(self.top_k):
                expert_idx = topk_indices[b, i].item()
                expert = self.prefetch_buffer[expert_idx]
                out[b] += topk_probs[b, i] * expert(x[b])
        return out

if __name__ == "__main__":
    model = BaselineMoEPrefetch()
    x = torch.randn(4, 512)
    y = model(x)
    print("Baseline MoE Prefetch executed successfully.")
