import torch
import torch.nn as nn
import torch.nn.functional as F

class W4A4Linear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super(W4A4Linear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter('bias', None)
            
    def quantize_w4(self, w):
        scale = w.abs().max() / 7.0
        q_w = torch.round(w / scale).clamp(-8, 7)
        return q_w * scale

    def quantize_a4(self, x):
        scale = x.abs().max() / 7.0
        q_x = torch.round(x / scale).clamp(-8, 7)
        return q_x * scale

    def forward(self, x):
        q_w = self.quantize_w4(self.weight)
        q_x = self.quantize_a4(x)
        return F.linear(q_x, q_w, self.bias)

if __name__ == "__main__":
    layer = W4A4Linear(128, 64)
    x = torch.randn(32, 128)
    out = layer(x)
    print(f"Output shape: {out.shape}")
