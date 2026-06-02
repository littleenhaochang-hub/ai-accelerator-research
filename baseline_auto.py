import torch
import torch.nn as nn

class W4A4_QJL_MoE_Prefetch_Baseline(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(128, 512)
        self.fc2 = nn.Linear(512, 128)
        
    def forward(self, x):
        # Simulated Test-Time Compute branching and W4A4 QJL
        return self.fc2(torch.relu(self.fc1(x)))

if __name__ == "__main__":
    model = W4A4_QJL_MoE_Prefetch_Baseline()
    print("Baseline prototype loaded.")
