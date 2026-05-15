import torch
import torch.nn as nn

class TTCMoEPrefetchBaseline(nn.Module):
    def __init__(self, d_model=512, num_experts=8, top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts)
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])

    def forward(self, x):
        # Bottleneck: sequential routing and synchronous expert fetching
        router_logits = self.router(x)
        routing_weights = torch.softmax(router_logits, dim=-1)
        top_weights, top_indices = torch.topk(routing_weights, self.top_k, dim=-1)
        
        out = torch.zeros_like(x)
        for i in range(x.size(0)):
            for j in range(self.top_k):
                expert_idx = top_indices[i, j].item()
                expert_out = self.experts[expert_idx](x[i].unsqueeze(0))
                out[i] += top_weights[i, j] * expert_out.squeeze(0)
        return out

if __name__ == "__main__":
    model = TTCMoEPrefetchBaseline()
    dummy_input = torch.randn(16, 512)
    output = model(dummy_input)
    print("Baseline executed successfully. Output shape:", output.shape)
