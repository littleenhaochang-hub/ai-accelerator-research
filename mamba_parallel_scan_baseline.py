import torch
import torch.nn as nn

class MambaParallelScanBaseline(nn.Module):
    def __init__(self, d_model=1024, d_state=16):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        
    def forward(self, x, dt, A, B, C):
        # Baseline pure-PyTorch non-hardware optimized parallel scan
        # Focus on memory bounds
        seq_len = x.shape[1]
        batch_size = x.shape[0]
        
        # simulated state progression
        h = torch.zeros(batch_size, self.d_model, self.d_state, device=x.device)
        ys = []
        for i in range(seq_len):
            # Bottleneck: memory bandwidth bound, low compute intensity
            dx = x[:, i]
            # State update
            h = h * A + B * dx.unsqueeze(-1)
            y = (h * C).sum(dim=-1)
            ys.append(y)
            
        return torch.stack(ys, dim=1)

if __name__ == "__main__":
    model = MambaParallelScanBaseline()
    x = torch.randn(2, 128, 1024)
    dt = torch.randn(2, 128, 1024)
    A = torch.randn(1024, 16)
    B = torch.randn(1024, 16)
    C = torch.randn(1024, 16)
    y = model(x, dt, A, B, C)
    print("Mamba Parallel Scan Baseline Initialized. Memory bandwidth bottleneck identified.")