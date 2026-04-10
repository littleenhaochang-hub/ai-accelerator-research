import torch
import torch.nn as nn

class TTC_MoE_Accelerator(nn.Module):
    def __init__(self):
        super().__init__()
        self.prefetch_buffer = nn.Parameter(torch.randn(128, 512))
    def forward(self, x):
        return x @ self.prefetch_buffer.T

