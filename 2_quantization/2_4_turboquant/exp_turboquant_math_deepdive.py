import torch
import math

def run_turboquant_math_deepdive():
    torch.manual_seed(42)
    torch.set_printoptions(precision=4, sci_mode=False)
    
    D = 16  # Small dimension for printable tensors
    
    print("=========================================================")
    print(" TURBOQUANT MATHEMATICS & CODE EXECUTION DEEP-DIVE")
    print("=========================================================\n")
    
    # ---------------------------------------------------------
    # 1. The Input Activation (with Outlier)
    # ---------------------------------------------------------
    X = torch.randn(1, D)
    X[0, 5] = 25.0  # Inject massive outlier
    
    print("1. Original Activation X (Notice the outlier at index 5):")
    print(X)
    print(f"   Max Absolute Value : {X.abs().max().item():.4f}")
    print(f"   Variance           : {X.var().item():.4f}\n")
    
    # ---------------------------------------------------------
    # 2. The Orthogonal Rotation Matrix (R)
    # ---------------------------------------------------------
    # Math: R^T * R = I
    R, _ = torch.linalg.qr(torch.randn(D, D))
    
    # Verify orthogonality
    identity_check = torch.matmul(R.T, R)
    is_orthogonal = torch.allclose(identity_check, torch.eye(D), atol=1e-5)
    
    print("2. Orthogonal Rotation Matrix R:")
    print(f"   Shape: {R.shape}")
    print(f"   Is Orthogonal (R^T * R == I)? {is_orthogonal}\n")
    
    # ---------------------------------------------------------
    # 3. The Rotation (Smearing the Outlier)
    # ---------------------------------------------------------
    # Math: X_rot = X * R
    X_rot = torch.matmul(X, R)
    
    print("3. Rotated Activation X_rot (Outlier is smeared!):")
    print(X_rot)
    print(f"   New Max Absolute Value : {X_rot.abs().max().item():.4f} (Massively reduced!)")
    print(f"   Variance               : {X_rot.var().item():.4f} (Energy is preserved)\n")
    
    # ---------------------------------------------------------
    # 4. 4-Bit Uniform Quantization
    # ---------------------------------------------------------
    # Math: s = max(|X_rot|) / (2^(b-1) - 1) = max(|X_rot|) / 7
    #       X_q = round(X_rot / s) * s
    scale_4bit = X_rot.abs().max() / 7.0
    X_q_int = torch.round(X_rot / scale_4bit).clamp(-8, 7)
    X_q = X_q_int * scale_4bit
    
    print("4. 4-Bit Quantized X_q:")
    print(f"   Scale factor (s) : {scale_4bit.item():.4f}")
    print(f"   Integer bounds   : [{X_q_int.min().item()}, {X_q_int.max().item()}]")
    
    # ---------------------------------------------------------
    # 5. The 1-Bit QJL Residual
    # ---------------------------------------------------------
    # Math: E = X_rot - X_q
    #       alpha = mean(|E|)
    #       E_1bit = sign(E) * alpha
    E = X_rot - X_q
    
    sign_E = torch.sign(E)
    sign_E[sign_E == 0] = 1.0  # Pack into 1-bit hardware logic
    
    alpha = E.abs().mean()
    E_1bit = sign_E * alpha
    
    print("\n5. 1-Bit QJL Residual E_1bit:")
    print(f"   Mean Absolute Error (alpha) : {alpha.item():.4f}")
    print(f"   1-Bit Array (Signs)         : {sign_E.tolist()[0]}")
    
    # ---------------------------------------------------------
    # 6. Reconstruction & Un-rotation
    # ---------------------------------------------------------
    # Math: X_rec = (X_q + E_1bit) * R^T
    X_rot_reconstructed = X_q + E_1bit
    X_reconstructed = torch.matmul(X_rot_reconstructed, R.T)
    
    print("\n6. Final Reconstructed X (After Inverse Rotation):")
    print(X_reconstructed)
    
    # Calculate SNR
    noise = X - X_reconstructed
    snr = 10 * math.log10(torch.mean(X**2).item() / torch.mean(noise**2).item())
    print(f"\nFinal Reconstruction SNR: {snr:.2f} dB")
    print("=========================================================")

if __name__ == "__main__":
    run_turboquant_math_deepdive()
