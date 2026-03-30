import torch
import torch.nn.functional as F

def quantize_4bit_symmetric(x):
    """Simulates 4-bit symmetric quantization per-token (dim=-1)."""
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x / scale).clamp(-8, 7)
    return x_q * scale

def calculate_snr(ref, approx):
    """Calculate Signal-to-Noise Ratio in dB."""
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()

def run_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, d_model = 1, 256, 128
    
    print(f"Initializing Full Attention Fusion Experiment (Seq: {seq_len}, Dim: {d_model})")
    
    # 1. Generate Q, K, V with extreme outliers
    Q = torch.randn(batch_size, seq_len, d_model)
    K = torch.randn(batch_size, seq_len, d_model)
    V = torch.randn(batch_size, seq_len, d_model)
    
    # Inject massive outliers
    Q[..., 10] *= 15.0; K[..., 10] *= 15.0; V[..., 10] *= 15.0
    Q[..., 42] *= 10.0; K[..., 42] *= 10.0; V[..., 42] *= 10.0

    # 2. Random orthogonal rotation matrix R
    R, _ = torch.linalg.qr(torch.randn(d_model, d_model))
    
    # --- Baseline: FP32 Exact Attention ---
    S_exact = torch.matmul(Q, K.transpose(-1, -2)) / (d_model ** 0.5)
    P_exact = F.softmax(S_exact, dim=-1)
    O_exact = torch.matmul(P_exact, V)

    # --- Experiment A: Naive A4 (No Rotation, FP32 KV) ---
    Q_a4 = quantize_4bit_symmetric(Q)
    S_a4 = torch.matmul(Q_a4, K.transpose(-1, -2)) / (d_model ** 0.5)
    P_a4 = F.softmax(S_a4, dim=-1)
    O_a4 = torch.matmul(P_a4, V)

    # --- Experiment B: TurboQuant KV Only (Rotated K4/V4, FP32 Q) ---
    Q_rot = torch.matmul(Q, R.transpose(-1, -2))
    K_rot = torch.matmul(K, R.transpose(-1, -2))
    V_rot = torch.matmul(V, R.transpose(-1, -2))
    
    K_rot_q4 = quantize_4bit_symmetric(K_rot)
    V_rot_q4 = quantize_4bit_symmetric(V_rot)
    
    S_tq = torch.matmul(Q_rot, K_rot_q4.transpose(-1, -2)) / (d_model ** 0.5)
    P_tq = F.softmax(S_tq, dim=-1)
    O_tq_rot = torch.matmul(P_tq, V_rot_q4)
    # Inverse rotation: O = O_rot * R
    O_tq = torch.matmul(O_tq_rot, R)

    # --- Experiment C: Fused A4 + TurboQuant KV ---
    Q_rot_q4 = quantize_4bit_symmetric(Q_rot)
    S_fused = torch.matmul(Q_rot_q4, K_rot_q4.transpose(-1, -2)) / (d_model ** 0.5)
    P_fused = F.softmax(S_fused, dim=-1)
    O_fused_rot = torch.matmul(P_fused, V_rot_q4)
    O_fused = torch.matmul(O_fused_rot, R)

    print("\n--- Phase 1: Attention Logit SNR (Before Softmax) ---")
    print(f"1. Naive A4 Only            : {calculate_snr(S_exact, S_a4):.2f} dB")
    print(f"2. TurboQuant KV Only       : {calculate_snr(S_exact, S_tq):.2f} dB")
    print(f"3. Fused A4 + TurboQuant KV : {calculate_snr(S_exact, S_fused):.2f} dB")
    
    print("\n--- Phase 2: Final Output SNR (After Softmax & V Projection) ---")
    print(f"1. Naive A4 Only            : {calculate_snr(O_exact, O_a4):.2f} dB")
    print(f"2. TurboQuant KV Only       : {calculate_snr(O_exact, O_tq):.2f} dB")
    print(f"3. Fused A4 + TurboQuant KV : {calculate_snr(O_exact, O_fused):.2f} dB")

    print("\n--- Observations ---")
    print("Notice the severe drop in dB between Phase 1 and Phase 2.")
    print("The Softmax function acts as a non-linear error amplifier. Because it is an exponential")
    print("function, errors in the logits shift the probability mass heavily. A small logit error")
    print("can cause the attention head to 'look' at the wrong token entirely, carrying the wrong V.")

if __name__ == "__main__":
    run_experiment()
