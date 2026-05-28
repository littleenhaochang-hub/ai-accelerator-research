import torch
import torch.nn as nn

class W4A4QJLBaseline(nn.Module):
    def __init__(self, hidden_size=4096):
        super().__init__()
        self.hidden_size = hidden_size
        self.w = nn.Parameter(torch.randn(hidden_size, hidden_size))
        
    def forward(self, x):
        # Simulate W4A4 quantization and QJL mapping
        # 1. Activation quantization (simulated)
        a_quant = torch.round(x * 7) / 7
        # 2. Weight quantization (simulated)
        w_quant = torch.round(self.w * 7) / 7
        # 3. Dense MATMUL
        out = torch.matmul(a_quant, w_quant)
        return out

if __name__ == "__main__":
    model = W4A4QJLBaseline()
    x = torch.randn(1, 4096)
    out = model(x)
    print(f"Prototype output shape: {out.shape}")