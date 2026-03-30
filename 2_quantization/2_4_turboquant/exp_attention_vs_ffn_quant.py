import torch
import torch.nn.functional as F

def quantize_4bit_tokenwise(x):
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    return torch.round(x / scale).clamp(-8, 7) * scale

def quantize_4bit_subchannel_fp16(x, group_size=32):
    shape = x.shape
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    scale = x_g.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x_g / scale).clamp(-8, 7) * scale
    return x_q.view(*shape)

def quantize_4bit_subchannel_e8m0(x, group_size=32):
    shape = x.shape
    x_g = x.view(*shape[:-1], shape[-1] // group_size, group_size)
    max_val = x_g.abs().max(dim=-1, keepdim=True).values
    max_val = torch.clamp(max_val, min=1e-5)
    ideal_scale = max_val / 7.0
    exponent = torch.ceil(torch.log2(ideal_scale))
    scale_e8m0 = torch.pow(2.0, exponent)
    x_q = torch.round(x_g / scale_e8m0).clamp(-8, 7) * scale_e8m0
    return x_q.view(*shape)

def get_rot_matrix(dim):
    torch.manual_seed(42)
    R, _ = torch.linalg.qr(torch.randn(dim, dim))
    return R

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    return (10 * torch.log10(signal_power / noise_power)).item()

def evaluate_tensor(X, name, R):
    snr_naive = calculate_snr(X, quantize_4bit_tokenwise(X))
    
    # TurboQuant
    X_rot = torch.matmul(X, R)
    X_rot_q = quantize_4bit_tokenwise(X_rot)
    X_tq = torch.matmul(X_rot_q, R.T)
    snr_tq = calculate_snr(X, X_tq)
    
    # Sub-channel FP16
    snr_sub_fp16 = calculate_snr(X, quantize_4bit_subchannel_fp16(X, 32))
    
    # Sub-channel E8M0
    snr_sub_e8m0 = calculate_snr(X, quantize_4bit_subchannel_e8m0(X, 32))
    
    print(f"\n=== {name} Matrix SNR ===")
    print(f"1. Naive 4-Bit (Token-wise) : {snr_naive:>6.2f} dB")
    print(f"2. TurboQuant (Rotation)    : {snr_tq:>6.2f} dB")
    print(f"3. Sub-Channel (FP16, G=32) : {snr_sub_fp16:>6.2f} dB")
    print(f"4. Sub-Channel (E8M0, G=32) : {snr_sub_e8m0:>6.2f} dB")

def run_dual_experiment():
    torch.manual_seed(42)
    batch, seq = 1, 256
    d_model = 4096
    d_ffn = 11008  # Typical LLaMA/Qwen expansion ratio
    
    print("Evaluating Quantization Resilience: Attention vs. FFN Activations")
    
    # ---------------------------------------------------------
    # 1. ATTENTION ACTIVATION SIMULATION (e.g., input to Q/K/V proj)
    # ---------------------------------------------------------
    # Attention inputs are typically LayerNormed, mostly Gaussian, with 
    # occasional mild contextual outliers.
    X_attn = torch.randn(batch, seq, d_model)
    X_attn[..., 15] *= 10.0
    X_attn[..., 1024] *= 15.0
    
    R_attn = get_rot_matrix(d_model)
    evaluate_tensor(X_attn, "ATTENTION (d_model=4096, Mild Outliers)", R_attn)
    
    # ---------------------------------------------------------
    # 2. FFN ACTIVATION SIMULATION (e.g., input to Down_proj)
    # ---------------------------------------------------------
    # FFN inputs (after Gate_proj * Up_proj + SiLU) are notoriously asymmetric.
    # SiLU zeroes out many negative values, creating a heavily skewed positive 
    # distribution. Furthermore, specific feature channels become massive, 
    # structural outliers (often > 100.0 magnitude).
    X_ffn_pre = torch.randn(batch, seq, d_ffn) * 2.0
    X_ffn = F.silu(X_ffn_pre) # Apply non-linearity
    
    # Inject massive structural, channel-wise outliers (typical in FFNs)
    X_ffn[..., 128] = 120.0
    X_ffn[..., 4096] = 85.0
    X_ffn[..., 8192] = 150.0
    
    R_ffn = get_rot_matrix(d_ffn)
    evaluate_tensor(X_ffn, "FFN Post-SiLU (d_ffn=11008, Massive Skew & Structural Outliers)", R_ffn)

if __name__ == "__main__":
    run_dual_experiment()
