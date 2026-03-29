import torch
import torch.nn as nn

class AttentionRouter(nn.Module):
    def __init__(self, dim, num_heads, num_routes):
        super().__init__()
        self.num_heads = num_heads
        self.num_routes = num_routes
        self.route_proj = nn.Linear(dim, num_routes)
        
    def forward(self, x):
        # x: [batch, seq, dim]
        routes = torch.softmax(self.route_proj(x), dim=-1)
        # route to specific heads/paths
        return routes

print("Attention Routing Baseline Initialized.")
