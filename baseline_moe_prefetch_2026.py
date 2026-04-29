import torch
import torch.nn as nn

class MoEBaseline(nn.Module):
    def __init__(self, hidden_size=1024, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(hidden_size, num_experts, bias=False)
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])
        
    def forward(self, x):
        # x: (batch_size, seq_len, hidden_size)
        gate_logits = self.gate(x)
        weights, indices = torch.topk(gate_logits, self.top_k, dim=-1)
        weights = torch.softmax(weights, dim=-1)
        
        out = torch.zeros_like(x)
        # Baseline iteration without prefetching
        for b in range(x.size(0)):
            for s in range(x.size(1)):
                for k in range(self.top_k):
                    expert_idx = indices[b, s, k].item()
                    w = weights[b, s, k]
                    expert_out = self.experts[expert_idx](x[b, s].unsqueeze(0))
                    out[b, s] += w * expert_out.squeeze(0)
        return out

if __name__ == "__main__":
    model = MoEBaseline()
    x = torch.randn(2, 16, 1024)
    print("Baseline MoE Output:", model(x).shape)
