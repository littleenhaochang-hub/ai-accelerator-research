import torch
import torch.nn as nn

class TTCSIMDDivergenceBaseline(nn.Module):
    def __init__(self, hidden_dim, max_thought_steps):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.max_thought_steps = max_thought_steps
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 4),
            nn.SiLU(),
            nn.Linear(hidden_dim * 4, hidden_dim)
        )
        self.router = nn.Linear(hidden_dim, 1) # Predicts if more thought is needed
        
    def forward(self, x, mask):
        # x shape: [batch_size, seq_len, hidden_dim]
        # Simulate SIMD divergence in Test-Time Compute
        batch_size = x.size(0)
        active_mask = torch.ones(batch_size, dtype=torch.bool, device=x.device)
        
        # In a real hardware accelerator, divergence here causes MAC array underutilization
        # and uncoalesced memory reads as active mask becomes sparse.
        for step in range(self.max_thought_steps):
            if not active_mask.any():
                break
                
            # Compute only for active lanes (naively mapped, causes divergence)
            # Hardware bottleneck: SRAM bank conflicts when scattering/gathering sparse active tokens
            active_x = x[active_mask] 
            
            # Heavy compute phase
            processed = self.ffn(active_x)
            x[active_mask] = processed
            
            # Routing phase: check if lane is done thinking
            router_logits = self.router(processed).squeeze(-1)
            continue_thinking = torch.sigmoid(router_logits) > 0.5
            
            # Update mask (divergence occurs here)
            active_mask[active_mask.clone()] = continue_thinking
            
        return x

if __name__ == "__main__":
    model = TTCSIMDDivergenceBaseline(hidden_dim=4096, max_thought_steps=16)
    dummy_input = torch.randn(32, 1, 4096)
    dummy_mask = torch.ones(32, 1)
    output = model(dummy_input, dummy_mask)
    print(f"Forward pass complete. Output shape: {output.shape}")
