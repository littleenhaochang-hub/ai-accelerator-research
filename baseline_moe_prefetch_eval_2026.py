import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, hidden_dim=1024, num_experts=8, top_k=2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(hidden_dim, num_experts)
        self.experts = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)])

    def forward(self, x):
        # x shape: [batch_size, seq_len, hidden_dim]
        routing_logits = self.router(x)
        routing_probs = torch.softmax(routing_logits, dim=-1)
        topk_probs, topk_indices = torch.topk(routing_probs, self.top_k, dim=-1)
        
        output = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = topk_indices[..., i]
            prob = topk_probs[..., i:i+1]
            # Bottleneck: In real HW, this sparse access causes prefetching stalls
            # We simulate the compute here
            for e_idx in range(self.num_experts):
                mask = (expert_idx == e_idx).unsqueeze(-1)
                if mask.any():
                    output += mask * self.experts[e_idx](x) * prob
                    
        return output

if __name__ == "__main__":
    model = MoEPrefetchBaseline()
    dummy_input = torch.randn(2, 64, 1024)
    out = model(dummy_input)
    print("Baseline MoE Prefetching simulated output shape:", out.shape)
