import torch
import torch.nn as nn
import time

def parallel_scan_prototype(u, dt, A, B, C, D):
    """
    Simulated parallel associative scan for Mamba-style SSMs.
    In a real implementation, this would be a custom Triton or Metal kernel
    using a parallel prefix sum algorithm (e.g., Blelloch scan).
    """
    batch, seq_len, d_model = u.shape
    d_state = A.shape[1]
    
    # We'll simulate the O(log N) parallel scan behavior by doing a block-wise or chunked scan
    # For now, we use a naive sequential loop but structure it to represent the work
    # of a parallel scan kernel (avoiding full O(N) sequential dependency if possible,
    # though PyTorch requires sequential for this prototype without custom CUDA/Triton).
    
    # Discretize A and B (Zero-order hold approximation)
    delta_A = torch.exp(torch.einsum('b l d, d n -> b l d n', dt, A))
    delta_B = torch.einsum('b l d, d n -> b l d n', dt, B)
    
    # u_proj: (batch, seq_len, d_model, d_state)
    u_proj = torch.einsum('b l d, b l d n -> b l d n', u, delta_B)
    
    # Sequential scan (simulating parallel kernel overhead)
    state = torch.zeros(batch, d_model, d_state, device=u.device)
    ys = []
    
    # In Triton, this loop is parallelized across sequence chunks
    for t in range(seq_len):
        state = delta_A[:, t] * state + u_proj[:, t]
        # y: (batch, d_model)
        y = torch.einsum('b d n, d n -> b d', state, C)
        ys.append(y)
        
    y_out = torch.stack(ys, dim=1) # (batch, seq_len, d_model)
    
    # Add skip connection
    out = y_out + u * D
    return out

class FastMambaPrototype(nn.Module):
    def __init__(self, d_model, d_state):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.A = nn.Parameter(torch.randn(d_model, d_state))
        self.B = nn.Parameter(torch.randn(d_model, d_state))
        self.C = nn.Parameter(torch.randn(d_model, d_state))
        self.D = nn.Parameter(torch.randn(d_model))
        self.dt_proj = nn.Linear(d_model, d_model)
        
    def forward(self, u):
        dt = torch.nn.functional.softplus(self.dt_proj(u))
        return parallel_scan_prototype(u, dt, self.A, self.B, self.C, self.D)

if __name__ == "__main__":
    d_model = 256
    d_state = 16
    seq_len = 4096
    batch = 1
    
    print(f"Testing Simulated Parallel Scan (seq_len={seq_len}, d_model={d_model}, d_state={d_state})...")
    model = FastMambaPrototype(d_model, d_state)
    x = torch.randn(batch, seq_len, d_model)
    
    t0 = time.time()
    with torch.no_grad():
        out = model(x)
    t1 = time.time()
    
    print(f"Simulated Parallel Scan Pass Time: {t1 - t0:.4f}s")
    print("Next step: Port `parallel_scan_prototype` to a Triton/Metal kernel to achieve true O(log N) depth and hardware-level parallelism.")
