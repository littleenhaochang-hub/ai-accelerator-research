import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    """
    Baseline for MoE Prefetching bottleneck during speculative decoding/TTC.
    Simulates the SRAM latency when expert routes are computed at the exact layer,
    leaving zero cycles to prefetch the weights from HBM to SRAM.
    """
    def __init__(self, d_model=4096, num_experts=8, top_k=2):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts)
        # Mocking HBM latency stall
        self.hbm_latency_cycles = 150
        
    def forward(self, x):
        # x shape: (batch, seq_len, d_model)
        # 1. Routing calculation
        route_logits = self.router(x)
        route_probs = torch.softmax(route_logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(route_probs, self.top_k, dim=-1)
        
        # 2. BOTTLENECK: At this exact clock cycle, we finally know which experts to fetch.
        # This forces a pipeline stall equal to hbm_latency_cycles before MAC arrays can compute.
        stall_cycles = self.hbm_latency_cycles
        
        return top_k_indices, stall_cycles

if __name__ == "__main__":
    model = MoEPrefetchBaseline()
    dummy_input = torch.randn(1, 1, 4096)
    indices, stall = model(dummy_input)
    print(f"Routed Experts: {indices.tolist()}, Pipeline Stalled for: {stall} cycles.")
