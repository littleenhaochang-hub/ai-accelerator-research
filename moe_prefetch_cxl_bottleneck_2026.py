import torch
import torch.nn as nn
import time

class CXLMoEPrefetchSim(nn.Module):
    def __init__(self, num_experts=8, embed_dim=1024, cxl_bw_gbps=64):
        super().__init__()
        self.num_experts = num_experts
        self.embed_dim = embed_dim
        # Simulate expert weights residing in slow CXL-attached memory
        self.expert_weights_size_mb = (embed_dim * embed_dim * 2) / (1024*1024) 
        self.cxl_bw_gbps = cxl_bw_gbps
        
    def forward(self, x, routing_probs):
        # x: [batch, seq, embed_dim]
        # routing_probs: [batch, seq, num_experts]
        
        # Determine top-1 expert for each token
        top_expert = torch.argmax(routing_probs, dim=-1)
        
        # Simulate CXL prefetch delay
        unique_experts = torch.unique(top_expert)
        data_to_fetch_mb = len(unique_experts) * self.expert_weights_size_mb
        transfer_time_sec = (data_to_fetch_mb * 8) / (self.cxl_bw_gbps * 1024)
        
        # Stall cycle simulation
        time.sleep(min(transfer_time_sec, 0.01)) # Cap sleep for fast execution
        
        # Dummy computation
        out = x * 0.99 
        return out, transfer_time_sec

if __name__ == "__main__":
    sim = CXLMoEPrefetchSim()
    x = torch.randn(1, 128, 1024)
    probs = torch.softmax(torch.randn(1, 128, 8), dim=-1)
    out, stall = sim(x, probs)
    print(f"MoE CXL Prefetch Simulation Complete. Stall time: {stall:.6f} s")
