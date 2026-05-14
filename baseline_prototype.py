import torch
import torch.nn as nn

class MoEPrefetchBaseline(nn.Module):
    def __init__(self):
        super().__init__()
        self.router = nn.Linear(1024, 8)
    def forward(self, x):
        return self.router(x)

