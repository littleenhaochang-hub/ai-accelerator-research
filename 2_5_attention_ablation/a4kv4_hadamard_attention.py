import torch
import torch.nn.functional as F
from scipy.linalg import hadamard
import math

def get_normalized_hadamard(dim):
    # Dim must be a power of 2
    h = torch.tensor(hadamard(dim), dtype=torch.float32)
    return h / math.sqrt(dim)

def fake_quantize_4bit(tensor):
    # Fake 4-bit asymmetric quantization
    # Map min/max to 0-15
    qmin, qmax = 0, 15
    min_val = tensor.min(dim=-1, keepdim=True)[0]
    max_val = tensor.max(dim=-1, keepdim=True)[0]
    scale = (max_val - min_val) / (qmax - qmin)
    scale = torch.clamp(scale, min=1e-5)
    
    q_tensor = torch.round((tensor - min_val) / scale)
    q_tensor = torch.clamp(q_tensor, qmin, qmax)
    
    dq_tensor = (q_tensor * scale) + min_val
    return dq_tensor

def prefill_attention_test():
    print("--- Prefill 2D Hadamard A4KV4 Attention ---")
    seq_len = 64
    d_model = 128
    
    # Random normal K and Q with some outliers to simulate LLM activations
    K = torch.randn(seq_len, d_model)
    K[10, 20] = 50.0  # outlier
    
    Q = torch.randn(1, d_model)
    Q[0, 20] = 30.0   # outlier
    
    # Baseline FP16 exact
    S_baseline = Q @ K.T
    
    # Hadamard Matrices
    H_token = get_normalized_hadamard(seq_len)
    H_feature = get_normalized_hadamard(d_model)
    
    # 2D Transform K (Left = Token, Right = Feature)
    K_2d = H_token @ K @ H_feature
    
    # Quantize K_2d to 4-bit and dequantize
    K_2d_q = fake_quantize_4bit(K_2d)
    
    # 1D Transform Q
    Q_trans = Q @ H_feature
    # No quantization on Q (kept in high precision)
    
    # Compressed space inner product
    S_prime = Q_trans @ K_2d_q.T
    
    # Reverse Hadamard on Token dimension to get true Attention
    S_approx = S_prime @ H_token.T  # Since symmetric, H_token.T == H_token
    
    # Metrics
    cos_sim = F.cosine_similarity(S_baseline.unsqueeze(0), S_approx.unsqueeze(0)).mean().item()
    snr = 10 * torch.log10(torch.sum(S_baseline**2) / torch.sum((S_baseline - S_approx)**2)).item()
    
    print(f"Cosine Similarity: {cos_sim:.4f}")
    print(f"SNR: {snr:.2f} dB")
    return cos_sim, snr

def decode_attention_test():
    print("\n--- Decode 1D Orthogonal A4KV4 Attention (Chunking) ---")
    d_model = 128
    
    # K is already stored and transformed (for simplicity, assuming 1D feature transform)
    # The mathematical proof in the prompt implies inner product invariance
    # Let's test just the Feature space orthogonal inner product
    
    K_vault = torch.randn(5000, d_model)
    K_vault[100, 50] = 40.0 # Outlier
    
    Q_new = torch.randn(1, d_model)
    Q_new[0, 50] = 30.0 # Outlier
    
    S_baseline = Q_new @ K_vault.T
    
    H_feature = get_normalized_hadamard(d_model)
    
    # K is stored with feature transform and quantized
    K_trans = K_vault @ H_feature
    K_trans_q = fake_quantize_4bit(K_trans)
    
    # New Q is transformed
    Q_trans = Q_new @ H_feature
    
    # Direct inner product
    S_approx = Q_trans @ K_trans_q.T
    
    cos_sim = F.cosine_similarity(S_baseline.unsqueeze(0), S_approx.unsqueeze(0)).mean().item()
    snr = 10 * torch.log10(torch.sum(S_baseline**2) / torch.sum((S_baseline - S_approx)**2)).item()
    
    print(f"Cosine Similarity: {cos_sim:.4f}")
    print(f"SNR: {snr:.2f} dB")

if __name__ == "__main__":
    prefill_attention_test()
    decode_attention_test()
