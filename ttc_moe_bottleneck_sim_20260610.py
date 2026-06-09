import torch
import torch.nn as nn
import time

class TTCMoEBottleneckSim(nn.Module):
    def __init__(self, hidden_dim=4096, num_experts=8, top_k=2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_experts = num_experts
        self.top_k = top_k
        self.experts = nn.ModuleList([
            nn.Linear(hidden_dim, hidden_dim) for _ in range(num_experts)
        ])
        self.router = nn.Linear(hidden_dim, num_experts)
        
    def forward(self, x, ttc_steps=3):
        # x: [batch_size, seq_len, hidden_dim]
        # Simulate TTC (Test-Time Compute) reasoning paths
        for step in range(ttc_steps):
            routing_logits = self.router(x)
            routing_probs = torch.softmax(routing_logits, dim=-1)
            top_probs, top_indices = torch.topk(routing_probs, self.top_k, dim=-1)
            
            out = torch.zeros_like(x)
            # Bottleneck: Uncoordinated expert fetching causing SRAM divergence
            for i in range(self.top_k):
                expert_idx = top_indices[:, :, i]
                # In hardware, this causes massive non-contiguous SRAM reads
                for b in range(x.size(0)):
                    for s in range(x.size(1)):
                        idx = expert_idx[b, s].item()
                        out[b, s] += top_probs[b, s, i] * self.experts[idx](x[b, s])
            x = x + out
        return x

if __name__ == "__main__":
    print("Simulating TTC MoE SRAM Divergence Bottleneck...")
    model = TTCMoEBottleneckSim()
    x = torch.randn(4, 128, 4096)
    start = time.time()
    out = model(x)
    end = time.time()
    print(f"Simulation complete in {end - start:.4f} seconds.")
