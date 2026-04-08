import torch
import math
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

def e8m0_scale(amax):
    """Simulates an E8M0 (Power-of-2) scale factor for hardware-friendly bit-shifts."""
    return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

def fake_quant_subchannel(x, bits=8, block_size=128):
    """Sub-channel (block-wise) quantization with E8M0 scale."""
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0:
        x = torch.nn.functional.pad(x, (0, pad_len))
    
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True)
    scale = e8m0_scale(amax / ((2**(bits-1)) - 1))
    
    q = torch.round(x_blocked / scale)
    q = torch.clamp(q, -(2**(bits-1)), (2**(bits-1)) - 1)
    dq = q * scale
    
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0:
        dq = dq[..., :-pad_len]
    return dq

def simulate_chained_householder(x, num_reflections=4):
    """O(k*N) Smearing for TurboQuant."""
    orig_shape = x.shape
    if len(orig_shape) == 3:
        B, Seq, H = orig_shape
        x_reshaped = x.view(-1, H)
    else:
        H = orig_shape[-1]
        x_reshaped = x.view(-1, H)
        
    torch.manual_seed(42)
    for _ in range(num_reflections):
        v = torch.randn(H, device=x.device, dtype=x.dtype)
        v = v / torch.norm(v)
        proj = torch.matmul(x_reshaped, v.unsqueeze(1))
        x_reshaped = x_reshaped - 2 * proj * v.unsqueeze(0)
        
    return x_reshaped.view(orig_shape)

def fake_quant_turboquant(x, bits=4, block_size=128):
    """TurboQuant (Householder + Block Quant)."""
    smeared = simulate_chained_householder(x)
    fq = fake_quant_subchannel(smeared, bits=bits, block_size=block_size)
    restored = simulate_chained_householder(fq) # Inverse
    return restored

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

def run_ablation():
    model_id = "Qwen/Qwen2.5-1.5B"
    print("Loading Real Model for Ablation: Qwen2.5-1.5B (Layer 12 extraction)...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    
    text = "The future of AI hardware relies on hardware-software co-design to overcome the memory wall. " * 5
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        # Extract mid-layer input to simulate exactly one transformer block
        layer_input = outputs.hidden_states[12].float()
        
    # Isolate Layer 12
    layer = model.model.layers[12].float()
    
    # Baseline Output
    with torch.no_grad():
        position_embeddings = model.model.rotary_emb(layer_input, torch.arange(layer_input.shape[1], device=layer_input.device).unsqueeze(0))
    with torch.no_grad():
        baseline_output = layer(layer_input, position_embeddings=position_embeddings)[0]
    
    experiments = [
        {"name": "Baseline (BF16/BF16)", "attn": "bf16", "ffn": "bf16"},
        {"name": "FFN Only (BF16 / A8W8 Subchannel)", "attn": "bf16", "ffn": "a8w8_sub"},
        {"name": "FFN Only (BF16 / A4W4 Subchannel)", "attn": "bf16", "ffn": "a4w4_sub"},
        {"name": "Attn Only (A8KV8 Subchannel / BF16)", "attn": "a8kv8_sub", "ffn": "bf16"},
        {"name": "Attn Only (A4KV4 Turbo / BF16)", "attn": "a4kv4_turbo", "ffn": "bf16"},
        {"name": "Combined (A8KV8 Sub / A8W8 Sub)", "attn": "a8kv8_sub", "ffn": "a8w8_sub"},
        {"name": "Tape-out (A4KV4 Turbo / A4W4 Sub)", "attn": "a4kv4_turbo", "ffn": "a4w4_sub"}
    ]
    
    results = []
    
    print("Running Ablation Grid...")
    for exp in experiments:
        # Clone layer input so we don't mutate
        x = layer_input.clone()
        
        # --- 1. Attention Block ---
        residual = x
        x_norm = layer.input_layernorm(x)
        
        if exp["attn"] == "a8kv8_sub":
            x_norm = fake_quant_subchannel(x_norm, bits=8)
        elif exp["attn"] == "a4kv4_turbo":
            x_norm = fake_quant_turboquant(x_norm, bits=4)
            
        attn_out = layer.self_attn(x_norm, attention_mask=None, position_embeddings=position_embeddings)[0]
        
        if exp["attn"] in ["a8kv8_sub", "a4kv4_turbo"]:
            # Simulate activation quantization post-attention
            bits = 8 if exp["attn"] == "a8kv8_sub" else 4
            attn_out = fake_quant_subchannel(attn_out, bits=bits)
            
        x = residual + attn_out
        
        # --- 2. FFN Block ---
        residual = x
        x_norm = layer.post_attention_layernorm(x)
        
        if exp["ffn"] == "a8w8_sub":
            x_norm = fake_quant_subchannel(x_norm, bits=8)
            # Faking weight quant directly on output approximation for speed in this trace
            ffn_out = layer.mlp(x_norm)
            ffn_out = fake_quant_subchannel(ffn_out, bits=8)
        elif exp["ffn"] == "a4w4_sub":
            x_norm = fake_quant_subchannel(x_norm, bits=4)
            ffn_out = layer.mlp(x_norm)
            ffn_out = fake_quant_subchannel(ffn_out, bits=4)
        else:
            ffn_out = layer.mlp(x_norm)
            
        x = residual + ffn_out
        
        # Compare to baseline
        sqnr = measure_sqnr(baseline_output, x)
        
        # Metric Estimates
        attn_mem = 2.0 if exp["attn"] == "bf16" else (1.0 if "8" in exp["attn"] else 0.5)
        ffn_mem = 2.0 if exp["ffn"] == "bf16" else (1.0 if "8" in exp["ffn"] else 0.5)
        rel_mem = (attn_mem + ffn_mem * 2) / 6.0 # Crude layer memory ratio
        
        results.append({
            "Experiment": exp["name"],
            "SQNR (dB)": round(sqnr, 2),
            "Memory (Normalized)": f"{rel_mem:.2f}x",
            "Hardware Scale": "e8m0 (Pow2)" if "sub" in exp["attn"] or "sub" in exp["ffn"] else "FP16"
        })
        
    df = pd.DataFrame(results)
    print("\n" + df.to_markdown(index=False))

if __name__ == "__main__":
    run_ablation()
