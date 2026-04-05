import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import matplotlib.pyplot as plt
import os

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def analyze_tensor_rank(tensor, threshold_ratio=0.95):
    """
    Analyzes the rank of a 2D tensor using SVD.
    Returns the effective rank needed to capture `threshold_ratio` of the energy (variance).
    """
    if tensor.dim() > 2:
        tensor = tensor.reshape(-1, tensor.shape[-1])
        
    # Convert to float32 for stable SVD
    tensor_f32 = tensor.to(torch.float32)
    
    # Compute SVD
    U, S, V = torch.svd(tensor_f32)
    
    # Calculate energy
    total_energy = torch.sum(S ** 2)
    cumulative_energy = torch.cumsum(S ** 2, dim=0)
    
    # Find rank needed to reach threshold
    effective_rank = torch.searchsorted(cumulative_energy, total_energy * threshold_ratio).item() + 1
    
    # Theoretical compression ratio = (M*R + R*N) / (M*N)
    # We invert it for "Compression Factor" = Original Size / Compressed Size
    M, N = tensor.shape
    original_size = M * N
    compressed_size = M * effective_rank + effective_rank * N
    compression_factor = original_size / compressed_size if compressed_size > 0 else 1.0
    
    return effective_rank, N, compression_factor, S

def run_low_rank_analysis():
    print(f"Loading {MODEL_ID} for KV Cache Low-Rank Analysis...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    
    # Generate a long context (simulating Vision/Long-Doc input)
    # We'll use a repeated text to build up a substantial KV cache
    base_text = "The quick brown fox jumps over the lazy dog. " * 50  # ~500 tokens
    inputs = tokenizer(base_text, return_tensors="pt").to(model.device)
    
    print(f"Sequence Length: {inputs.input_ids.shape[1]} tokens")
    
    # Run forward pass to extract KV cache
    with torch.no_grad():
        outputs = model(**inputs, use_cache=True)
        
    past_key_values = list(outputs.past_key_values)
    num_layers = len(past_key_values)
    
    print("\n=== KV Cache SVD Rank Analysis (Energy Threshold: 95%) ===")
    print(f"{'Layer':<8} | {'Type':<5} | {'Head':<5} | {'Orig Dim':<10} | {'Effective Rank':<15} | {'Compression Ratio':<18}")
    print("-" * 75)
    
    layer_compression_factors_k = []
    layer_compression_factors_v = []
    
    # We analyze a few sample layers (Early, Mid, Late) to save time
    target_layers = [0, num_layers // 2, num_layers - 1]
    
    for layer_idx in target_layers:
        # KV cache shape: (batch_size, num_heads, seq_len, head_dim)
        K_cache = past_key_values[layer_idx][0][0] # Drop batch dim -> (num_heads, seq_len, head_dim)
        V_cache = past_key_values[layer_idx][1][0]
        
        num_heads = K_cache.shape[0]
        
        # Analyze Head 0 for simplicity in the table
        head_idx = 0
        K_head = K_cache[head_idx] # (seq_len, head_dim)
        V_head = V_cache[head_idx]
        
        rank_k, dim_k, comp_k, _ = analyze_tensor_rank(K_head)
        rank_v, dim_v, comp_v, _ = analyze_tensor_rank(V_head)
        
        print(f"Layer {layer_idx:<2} | Key   | Head {head_idx} | {dim_k:<10} | {rank_k:<15} | {comp_k:.2f}x")
        print(f"Layer {layer_idx:<2} | Value | Head {head_idx} | {dim_v:<10} | {rank_v:<15} | {comp_v:.2f}x")
        
        layer_compression_factors_k.append(comp_k)
        layer_compression_factors_v.append(comp_v)
        
    avg_comp = (sum(layer_compression_factors_k) + sum(layer_compression_factors_v)) / 6
    print("-" * 75)
    print(f"Average Theoretical Compression Ratio via SVD (95% Energy): {avg_comp:.2f}x\n")

    print("=== Conclusion ===")
    if avg_comp > 1.5:
        print("✅ The Implicit Low-Rank hypothesis holds true! The KV Cache exhibits massive structural redundancy.")
        print("   This means we can compress KV cache by storing it as two smaller matrices (U * V^T) instead of one large matrix,")
        print("   breaking the memory bandwidth wall linearly BEFORE we even apply 4-bit quantization.")
    else:
        print("❌ The KV Cache is full rank. The SVD compression overhead exceeds the memory savings.")

if __name__ == "__main__":
    run_low_rank_analysis()
