import torch
import torch.nn.functional as F

def quantize_4bit_symmetric(x):
    """Simulates 4-bit symmetric quantization."""
    scale = x.abs().max(dim=-1, keepdim=True).values / 7.0
    scale = torch.clamp(scale, min=1e-5)
    x_q = torch.round(x / scale).clamp(-8, 7)
    return x_q * scale

def quantize_1bit_residual(x_original, x_quantized):
    """
    Simulates a 1-bit sign residual (QJL).
    Extracts the quantization error, compresses it to 1-bit (+1 / -1),
    and applies a per-token mean absolute scaling factor.
    """
    error = x_original - x_quantized
    # 1-bit quantization (sign only)
    sign_1bit = torch.sign(error)
    # Zeroes become +1 to maintain strict 1-bit hardware packing
    sign_1bit[sign_1bit == 0] = 1.0 
    
    # Per-token scaling factor (mean absolute error)
    scale = error.abs().mean(dim=-1, keepdim=True)
    
    return sign_1bit * scale

def calculate_snr(ref, approx):
    noise = ref - approx
    signal_power = torch.mean(ref ** 2)
    noise_power = torch.mean(noise ** 2)
    snr = 10 * torch.log10(signal_power / noise_power)
    return snr.item()

def run_experiment():
    torch.manual_seed(42)
    batch_size, seq_len, d_model = 1, 256, 128
    
    print(f"Initializing 1-Bit Residual (QJL) Recovery Experiment (Seq: {seq_len}, Dim: {d_model})")
    
    # 1. Generate Q, K, V with massive outliers
    Q = torch.randn(batch_size, seq_len, d_model)
    K = torch.randn(batch_size, seq_len, d_model)
    V = torch.randn(batch_size, seq_len, d_model)
    Q[..., 10] *= 15.0; K[..., 10] *= 15.0; V[..., 10] *= 15.0
    Q[..., 42] *= 10.0; K[..., 42] *= 10.0; V[..., 42] *= 10.0

    # 2. Random orthogonal rotation matrix R
    R, _ = torch.linalg.qr(torch.randn(d_model, d_model))
    
    # --- Exact FP32 Baseline ---
    S_exact = torch.matmul(Q, K.transpose(-1, -2)) / (d_model ** 0.5)
    O_exact = torch.matmul(F.softmax(S_exact, dim=-1), V)

    # --- Fused A4 + TurboQuant (No Residual) ---
    Q_rot = torch.matmul(Q, R.transpose(-1, -2))
    K_rot = torch.matmul(K, R.transpose(-1, -2))
    V_rot = torch.matmul(V, R.transpose(-1, -2))
    
    Q_rot_q4 = quantize_4bit_symmetric(Q_rot)
    K_rot_q4 = quantize_4bit_symmetric(K_rot)
    V_rot_q4 = quantize_4bit_symmetric(V_rot)
    
    S_fused = torch.matmul(Q_rot_q4, K_rot_q4.transpose(-1, -2)) / (d_model ** 0.5)
    O_fused_rot = torch.matmul(F.softmax(S_fused, dim=-1), V_rot_q4)
    O_fused = torch.matmul(O_fused_rot, R)

    # --- Fused A4 + TurboQuant + 1-Bit KV Residual (QJL) ---
    # Calculate the 1-bit residual for K and V
    K_res_1bit = quantize_1bit_residual(K_rot, K_rot_q4)
    V_res_1bit = quantize_1bit_residual(V_rot, V_rot_q4)
    
    # During hardware inference, this is computed as:
    # (Q4 @ K4.T) + (Q4 @ K_res_1bit.T) -> The second term uses ultra-fast bitwise popcount!
    S_qjl = torch.matmul(Q_rot_q4, (K_rot_q4 + K_res_1bit).transpose(-1, -2)) / (d_model ** 0.5)
    
    O_qjl_rot = torch.matmul(F.softmax(S_qjl, dim=-1), (V_rot_q4 + V_res_1bit))
    O_qjl = torch.matmul(O_qjl_rot, R)

    print("\n--- Phase 1: Attention Logit SNR (Before Softmax) ---")
    print(f"1. Fused A4 + TurboQuant (No Residual) : {calculate_snr(S_exact, S_fused):.2f} dB")
    print(f"2. Fused A4 + TurboQuant + 1-Bit QJL   : {calculate_snr(S_exact, S_qjl):.2f} dB")
    print(f"-> QJL Recovery: +{calculate_snr(S_exact, S_qjl) - calculate_snr(S_exact, S_fused):.2f} dB")

    print("\n--- Phase 2: Final Output SNR (After Softmax & V Projection) ---")
    print(f"1. Fused A4 + TurboQuant (No Residual) : {calculate_snr(O_exact, O_fused):.2f} dB")
    print(f"2. Fused A4 + TurboQuant + 1-Bit QJL   : {calculate_snr(O_exact, O_qjl):.2f} dB")
    print(f"-> QJL Recovery: +{calculate_snr(O_exact, O_qjl) - calculate_snr(O_exact, O_fused):.2f} dB")

    print("\n--- Hardware Implication ---")
    print("By adding a mere 1-bit per parameter (expanding 4-bit to effectively 5-bit memory footprint),")
    print("we use a bitwise XNOR/Popcount kernel to rescue the attention scores right before the Softmax cliff.")

if __name__ == "__main__":
    run_experiment()