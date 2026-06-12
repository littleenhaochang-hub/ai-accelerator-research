import torch
import torch.nn as nn

class BaselineMoE(nn.Module):
    def __init__(self, hidden_dim, num_experts, top_k):
        super().__init__()
        self.router = nn.Linear(hidden_dim, num_experts, bias=False)
        self.top_k = top_k

    def forward(self, x):
        # Bottleneck: Routing logic introduces a data dependency stall
        # waiting for expert selection before fetching expert weights from HBM.
        routing_logits = self.router(x)
        routing_probs, selected_experts = torch.topk(routing_logits, self.top_k, dim=-1)
        return routing_probs, selected_experts

if __name__ == "__main__":
    x = torch.randn(1, 128, 4096)
    moe = BaselineMoE(4096, 8, 2)
    probs, experts = moe(x)
    print("Baseline MoE executed. Simulated stall on expert load.")