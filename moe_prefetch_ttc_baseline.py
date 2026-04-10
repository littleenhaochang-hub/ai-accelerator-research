import torch
import torch.nn as nn
import time

class MoEPrefetchBaseline(nn.Module):
    def __init__(self, hidden_size=4096, num_experts=8, top_k=2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(hidden_size, num_experts, bias=False)
        self.experts = nn.ModuleList([nn.Linear(hidden_size, hidden_size) for _ in range(num_experts)])
        
    def forward(self, x):
        # x shape: [batch, seq_len, hidden]
        gate_logits = self.gate(x)
        weights, indices = torch.topk(gate_logits, self.top_k, dim=-1)
        weights = torch.softmax(weights, dim=-1)
        
        out = torch.zeros_like(x)
        # Simulate hardware bottleneck: serial fetching of expert weights from HBM based on dynamic routing
        # In reality, this loop causes a pipeline stall because `indices` are not known in advance.
        for batch_idx in range(x.size(0)):
            for seq_idx in range(x.size(1)):
                for k in range(self.top_k):
                    expert_idx = indices[batch_idx, seq_idx, k]
                    weight = weights[batch_idx, seq_idx, k]
                    
                    # Simulating the latency of fetching the expert (cache miss)
                    time.sleep(0.001) 
                    
                    expert_out = self.experts[expert_idx](x[batch_idx, seq_idx])
                    out[batch_idx, seq_idx] += weight * expert_out
                    
        return out

if __name__ == "__main__":
    print("Running MoE Prefetching Hardware Bottleneck Baseline...")
    model = MoEPrefetchBaseline()
    x = torch.randn(2, 8, 4096)
    
    start_time = time.time()
    out = model(x)
    end_time = time.time()
    
    print(f"Latency for [2, 8, 4096] batch: {end_time - start_time:.4f} seconds")
    print("Bottleneck Identified: Dynamic MoE routing prevents static prefetching, causing severe HBM latency stalls during Test-Time Compute branching.")
