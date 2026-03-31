import torch
import torch.nn.functional as F

# --- Quantization Methods ---
def quantize_4bit_naive(x):
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

def quantize_1bit_residual(x_orig, x_quant):
    err = x_orig - x_quant
    sign_1bit = torch.sign(err)
    sign_1bit[sign_1bit == 0] = 1.0
    scale = err.abs().mean(dim=-1, keepdim=True)
    return sign_1bit * scale

def get_rot_matrix(dim):
    torch.manual_seed(42)
    R, _ = torch.linalg.qr(torch.randn(dim, dim))
    return R

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    return (10 * torch.log10(signal_power / noise_power)).item()

def run_attention_ablation():
    torch.manual_seed(42)
    batch, seq, d_model = 1, 256, 128
    
    print(f"=== Attention Ablation Study: Towards A4 KV4 ===")
    print(f"Dim: {d_model} | Outliers Injected into Q, K, V\n")
    
    Q = torch.randn(batch, seq, d_model)
    K = torch.randn(batch, seq, d_model)
    V = torch.randn(batch, seq, d_model)
    
    # Inject mild to heavy outliers
    Q[..., 15] *= 10.0; K[..., 15] *= 10.0; V[..., 15] *= 10.0
    Q[..., 64] *= 15.0; K[..., 64] *= 15.0; V[..., 64] *= 15.0

    R = get_rot_matrix(d_model)
    
    # --- FP32 Exact Baseline ---
    S_exact = torch.matmul(Q, K.transpose(-1, -2)) / (d_model ** 0.5)
    O_exact = torch.matmul(F.softmax(S_exact, dim=-1), V)

    print("STAGE 1: KV CACHE QUANTIZATION (Q is FP32)")
    print("-" * 50)
    
    # 1.1 Naive KV4
    S_naive_kv = torch.matmul(Q, quantize_4bit_naive(K).transpose(-1, -2)) / (d_model ** 0.5)
    O_naive_kv = torch.matmul(F.softmax(S_naive_kv, dim=-1), quantize_4bit_naive(V))
    print(f"[KV4] Naive 4-bit           | SNR: {calculate_snr(O_exact, O_naive_kv):>6.2f} dB")
    
    # 1.2 Sub-Channel KV4 (FP16 Scale, G=32)
    K_sub = quantize_4bit_subchannel_fp16(K, 32)
    V_sub = quantize_4bit_subchannel_fp16(V, 32)
    S_sub_kv = torch.matmul(Q, K_sub.transpose(-1, -2)) / (d_model ** 0.5)
    O_sub_kv = torch.matmul(F.softmax(S_sub_kv, dim=-1), V_sub)
    print(f"[KV4] Sub-Channel (FP16)    | SNR: {calculate_snr(O_exact, O_sub_kv):>6.2f} dB")
    
    # 1.3 Sub-Channel KV4 (E8M0 Scale, G=32)
    K_sub_e8m0 = quantize_4bit_subchannel_e8m0(K, 32)
    V_sub_e8m0 = quantize_4bit_subchannel_e8m0(V, 32)
    S_sub_kv_e8m0 = torch.matmul(Q, K_sub_e8m0.transpose(-1, -2)) / (d_model ** 0.5)
    O_sub_kv_e8m0 = torch.matmul(F.softmax(S_sub_kv_e8m0, dim=-1), V_sub_e8m0)
    print(f"[KV4] Sub-Channel (E8M0)    | SNR: {calculate_snr(O_exact, O_sub_kv_e8m0):>6.2f} dB")
    
    # 1.4 TurboQuant KV4
    Q_rot = torch.matmul(Q, R.transpose(-1, -2))
    K_rot = torch.matmul(K, R.transpose(-1, -2))
    V_rot = torch.matmul(V, R.transpose(-1, -2))
    K_tq = quantize_4bit_naive(K_rot)
    V_tq = quantize_4bit_naive(V_rot)
    S_tq_kv = torch.matmul(Q_rot, K_tq.transpose(-1, -2)) / (d_model ** 0.5)
    O_tq_kv = torch.matmul(F.softmax(S_tq_kv, dim=-1), V_tq)
    O_tq_kv = torch.matmul(O_tq_kv, R)
    print(f"[KV4] TurboQuant (Rotation) | SNR: {calculate_snr(O_exact, O_tq_kv):>6.2f} dB")

    # 1.5 TurboQuant KV4 + 1-bit QJL
    K_qjl = K_tq + quantize_1bit_residual(K_rot, K_tq)
    V_qjl = V_tq + quantize_1bit_residual(V_rot, V_tq)
    S_tq_qjl_kv = torch.matmul(Q_rot, K_qjl.transpose(-1, -2)) / (d_model ** 0.5)
    O_tq_qjl_kv = torch.matmul(F.softmax(S_tq_qjl_kv, dim=-1), V_qjl)
    O_tq_qjl_kv = torch.matmul(O_tq_qjl_kv, R)
    print(f"[KV4] TurboQuant + 1-b QJL  | SNR: {calculate_snr(O_exact, O_tq_qjl_kv):>6.2f} dB")

    print("\nSTAGE 2: A4 KV4 FULL QUANTIZATION (Q is also Quantized)")
    print("-" * 50)
    
    # 2.1 Naive A4 KV4
    S_naive_a4 = torch.matmul(quantize_4bit_naive(Q), quantize_4bit_naive(K).transpose(-1, -2)) / (d_model ** 0.5)
    O_naive_a4 = torch.matmul(F.softmax(S_naive_a4, dim=-1), quantize_4bit_naive(V))
    print(f"[A4KV4] Naive 4-bit         | SNR: {calculate_snr(O_exact, O_naive_a4):>6.2f} dB")
    
    # 2.2 Sub-Channel A4 KV4 (FP16 Scale, G=32)
    Q_sub = quantize_4bit_subchannel_fp16(Q, 32)
    S_sub_a4 = torch.matmul(Q_sub, K_sub.transpose(-1, -2)) / (d_model ** 0.5)
    O_sub_a4 = torch.matmul(F.softmax(S_sub_a4, dim=-1), V_sub)
    print(f"[A4KV4] Sub-Channel (FP16)  | SNR: {calculate_snr(O_exact, O_sub_a4):>6.2f} dB")
    
    # 2.3 Sub-Channel A4 KV4 (E8M0 Scale, G=32)
    Q_sub_e8m0 = quantize_4bit_subchannel_e8m0(Q, 32)
    S_sub_a4_e8m0 = torch.matmul(Q_sub_e8m0, K_sub_e8m0.transpose(-1, -2)) / (d_model ** 0.5)
    O_sub_a4_e8m0 = torch.matmul(F.softmax(S_sub_a4_e8m0, dim=-1), V_sub_e8m0)
    print(f"[A4KV4] Sub-Channel (E8M0)  | SNR: {calculate_snr(O_exact, O_sub_a4_e8m0):>6.2f} dB")
    
    # 2.4 TurboQuant A4 KV4
    Q_tq = quantize_4bit_naive(Q_rot)
    S_tq_a4 = torch.matmul(Q_tq, K_tq.transpose(-1, -2)) / (d_model ** 0.5)
    O_tq_a4 = torch.matmul(F.softmax(S_tq_a4, dim=-1), V_tq)
    O_tq_a4 = torch.matmul(O_tq_a4, R)
    print(f"[A4KV4] TurboQuant          | SNR: {calculate_snr(O_exact, O_tq_a4):>6.2f} dB")

    # 2.5 TurboQuant A4 KV4 + 1-bit QJL (on KV)
    S_tq_qjl_a4 = torch.matmul(Q_tq, K_qjl.transpose(-1, -2)) / (d_model ** 0.5)
    O_tq_qjl_a4 = torch.matmul(F.softmax(S_tq_qjl_a4, dim=-1), V_qjl)
    O_tq_qjl_a4 = torch.matmul(O_tq_qjl_a4, R)
    print(f"[A4KV4] TurboQuant + 1-b QJL| SNR: {calculate_snr(O_exact, O_tq_qjl_a4):>6.2f} dB")

if __name__ == "__main__":
    run_attention_ablation()
