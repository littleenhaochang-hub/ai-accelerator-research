import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, d_model=4096, num_experts=8, prefetch_window=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.prefetch_window = prefetch_window
        # Mock experts
        self.experts = nn.ModuleList([nn.Linear(d_model, d_model) for _ in range(num_experts)])
        self.router = nn.Linear(d_model, num_experts)
        
    def forward(self, x):
        # x: [batch, seq, d_model]
        # Simulate router logits and bottleneck in prefetching
        router_logits = self.router(x)
        routing_probs = torch.softmax(router_logits, dim=-1)
        top_expert_indices = torch.argmax(routing_probs, dim=-1)
        
        # Simulating bottleneck: waiting for experts to be loaded from HBM/CXL
        # The auto-researcher will optimize this naive serial execution
        output = torch.zeros_like(x)
        for i in range(x.size(0)):
            for j in range(x.size(1)):
                expert_idx = top_expert_indices[i, j].item()
                output[i, j] = self.experts[expert_idx](x[i, j])
                
        return output

if __name__ == "__main__":
    model = MoEPrefetchBaseline()
    x = torch.randn(2, 128, 4096)
    y = model(x)
    print(f"Baseline executed. Output shape: {y.shape}")
