import torch
import torch.nn.functional as F

def quantize_4bit_naive(x):
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def quantize_4bit_percentile(x, p=0.99):
    x_f32 = x.float().abs()
    # Estimate the 99th percentile across the feature dimension
    clip_val = torch.quantile(x_f32, p, dim=-1, keepdim=True)
    clip_val = torch.clamp(clip_val, min=1e-5)
    x_clipped = torch.clamp(x, -clip_val.expand_as(x), clip_val.expand_as(x))
    scale = clip_val / 7.0
    return torch.round(x_clipped / scale).clamp(-8, 7) * scale

def quantize_4bit_group(x, group_size=32):
    shape = x.shape
    assert shape[-1] % group_size == 0
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    scale = x_g.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_g / scale).clamp(-8, 7) * scale
    return x_q.view(*shape)

def quantize_4bit_sparse_dense(x, threshold_percentile=0.99):
    x_f32 = x.float().abs()
    threshold = torch.quantile(x_f32, threshold_percentile, dim=-1, keepdim=True)
    sparse_mask = x_f32 > threshold
    dense_mask = ~sparse_mask
    
    x_dense = x * dense_mask
    scale = x_dense.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_dense / scale).clamp(-8, 7) * scale
    
    x_sparse = x * sparse_mask
    return x_q + x_sparse

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()

def run_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, d_model = 1, 256, 128
    
    print(f"Initializing A4A4 Optimization Math SNR (Seq: {seq_len}, Dim: {d_model})")
    
    Q = torch.randn(batch_size, seq_len, d_model)
    K = torch.randn(batch_size, seq_len, d_model)
    V = torch.randn(batch_size, seq_len, d_model)
    
    # Inject massive outliers
    Q[..., 10] *= 15.0; K[..., 10] *= 15.0; V[..., 10] *= 15.0
    Q[..., 42] *= 10.0; K[..., 42] *= 10.0; V[..., 42] *= 10.0
    
    # --- Exact FP32 Baseline ---
    S_exact = torch.matmul(Q, K.transpose(-1, -2)) / (d_model ** 0.5)
    O_exact = torch.matmul(F.softmax(S_exact, dim=-1), V)

    methods = {
        "1. Naive A4A4": quantize_4bit_naive,
        "2. Percentile Clipping (p=0.99)": lambda x: quantize_4bit_percentile(x, p=0.99),
        "3. Block/Group Quant (G=32)": lambda x: quantize_4bit_group(x, group_size=32),
        "4. Sparse-Dense Hybrid (p=0.99)": lambda x: quantize_4bit_sparse_dense(x, threshold_percentile=0.99)
    }

    print("\n--- Phase 1: Attention Logit SNR (Before Softmax) ---")
    results_s = {}
    for name, quant_func in methods.items():
        Q_q = quant_func(Q)
        K_q = quant_func(K)
        S_q = torch.matmul(Q_q, K_q.transpose(-1, -2)) / (d_model ** 0.5)
        snr = calculate_snr(S_exact, S_q)
        results_s[name] = S_q
        print(f"{name:<35}: {snr:>6.2f} dB")

    print("\n--- Phase 2: Final Output SNR (After Softmax & V Projection) ---")
    for name, quant_func in methods.items():
        V_q = quant_func(V)
        S_q = results_s[name]
        O_q = torch.matmul(F.softmax(S_q, dim=-1), V_q)
        snr = calculate_snr(O_exact, O_q)
        print(f"{name:<35}: {snr:>6.2f} dB")

if __name__ == "__main__":
    run_experiment()
