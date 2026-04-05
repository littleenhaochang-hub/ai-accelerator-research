import torch
import torch.nn as nn

class SimpleMoE(nn.Module):
    def __init__(self, d_model, num_experts, expert_dim):
        super().__init__()
        self.router = nn.Linear(d_model, num_experts)
        # Experts kept on CPU to simulate memory constraints
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, expert_dim),
                nn.ReLU(),
                nn.Linear(expert_dim, d_model)
            ).cpu() for _ in range(num_experts)
        ])
        self.num_experts = num_experts

    def forward(self, x):
        # x is on GPU ideally
        batch_size, seq_len, d_model = x.shape
        x_flat = x.view(-1, d_model)
        
        # Routing
        route_logits = self.router(x_flat)
        route_probs = torch.softmax(route_logits, dim=-1)
        top1_probs, top1_indices = torch.topk(route_probs, 1, dim=-1)
        
        output = torch.zeros_like(x_flat)
        
        # Simulate bottleneck: CPU-GPU transfer for each selected expert
        for i in range(self.num_experts):
            mask = (top1_indices == i).squeeze(-1)
            if mask.any():
                expert_input = x_flat[mask]
                
                # Fetch expert to GPU (simulated prefetch/transfer)
                expert = self.experts[i].to(x.device)
                
                expert_output = expert(expert_input)
                output[mask] = expert_output * top1_probs[mask]
                
                # Offload expert back to CPU
                expert.to('cpu')
                
        return output.view(batch_size, seq_len, d_model)

if __name__ == "__main__":
    d_model = 512
    num_experts = 8
    expert_dim = 2048
    model = SimpleMoE(d_model, num_experts, expert_dim).cuda()
    x = torch.randn(2, 64, d_model).cuda()
    out = model(x)
    print("Baseline MoE pass complete. Output shape:", out.shape)
