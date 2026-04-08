import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

# Standard NF4 (NormalFloat4) Quantiles
NF4_LUT = torch.tensor([
    -1.0, -0.6961928, -0.5250731, -0.3949175, -0.2844414, -0.1847734, -0.0910500, 0.0,
    0.0795803, 0.1609302, 0.2461123, 0.3379152, 0.4407098, 0.5626170, 0.7229568, 1.0
])

def fake_quant_nf4_lut(x, block_size=128):
    """Simulates a 4-bit LUT based quantization (like NF4)."""
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0:
        x = torch.nn.functional.pad(x, (0, pad_len))
        
    x_blocked = x.view(-1, block_size)
    
    # Scale by absolute maximum in the block
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True).clamp(min=1e-7)
    x_scaled = x_blocked / amax
    
    # Move LUT to correct device and type
    lut = NF4_LUT.to(device=x.device, dtype=x.dtype)
    
    # Broadcast and find nearest LUT index (simulating hardware comparator array)
    # x_scaled: [N, block_size, 1]
    # lut: [16]
    diffs = torch.abs(x_scaled.unsqueeze(-1) - lut)
    indices = torch.argmin(diffs, dim=-1)
    
    # Gather the quantized values
    q = lut[indices]
    
    # Dequantize
    dq = q * amax
    
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0:
        dq = dq[..., :-pad_len]
    return dq

def simulate_chained_householder(x, num_reflections=4):
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

def fake_quant_lut_turboquant(x, block_size=128):
    """LUT-based TurboQuant: Householder Smearing + NF4 LUT Quantization"""
    smeared = simulate_chained_householder(x)
    fq = fake_quant_nf4_lut(smeared, block_size=block_size)
    restored = simulate_chained_householder(fq)
    return restored

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

def run_lut_ablation():
    model_id = "Qwen/Qwen2.5-1.5B"
    print("Loading Real Model for LUT Ablation: Qwen2.5-1.5B (Layer 12 extraction)...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    
    text = "The future of AI hardware relies on hardware-software co-design to overcome the memory wall. " * 5
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        layer_input = outputs.hidden_states[12].float()
        
    layer = model.model.layers[12].float()
    
    with torch.no_grad():
        position_embeddings = model.model.rotary_emb(layer_input, torch.arange(layer_input.shape[1], device=layer_input.device).unsqueeze(0))
        baseline_output = layer(layer_input, position_embeddings=position_embeddings)[0]
    
    experiments = [
        {"name": "Tape-out Linear (A4KV4 Turbo / A4W4 Sub)", "attn": "linear", "ffn": "linear"},
        {"name": "Tape-out LUT (A4KV4 LUT-Turbo / A4W4 LUT)", "attn": "lut", "ffn": "lut"}
    ]
    
    results = []
    
    print("Running LUT vs Linear Grid...")
    for exp in experiments:
        x = layer_input.clone()
        
        # Attn
        residual = x
        x_norm = layer.input_layernorm(x)
        if exp["attn"] == "lut":
            x_norm = fake_quant_lut_turboquant(x_norm)
        else: # simulate the old linear turboquant we had
            smeared = simulate_chained_householder(x_norm)
            # Linear 4-bit subchannel
            blocked = smeared.view(-1, 128)
            scale = torch.amax(torch.abs(blocked), dim=-1, keepdim=True) / 7.0
            q = torch.clamp(torch.round(blocked / scale), -7, 7)
            linear_fq = (q * scale).view(smeared.shape)
            x_norm = simulate_chained_householder(linear_fq)
            
        attn_out = layer.self_attn(x_norm, attention_mask=None, position_embeddings=position_embeddings)[0]
        x = residual + attn_out
        
        # FFN
        residual = x
        x_norm = layer.post_attention_layernorm(x)
        if exp["ffn"] == "lut":
            x_norm = fake_quant_nf4_lut(x_norm)
            ffn_out = layer.mlp(x_norm)
            ffn_out = fake_quant_nf4_lut(ffn_out)
        else:
            # Linear 4-bit
            blocked = x_norm.view(-1, 128)
            scale = torch.amax(torch.abs(blocked), dim=-1, keepdim=True) / 7.0
            q = torch.clamp(torch.round(blocked / scale), -7, 7)
            x_norm = (q * scale).view(x_norm.shape)
            
            ffn_out = layer.mlp(x_norm)
            
            blocked_out = ffn_out.view(-1, 128)
            scale_out = torch.amax(torch.abs(blocked_out), dim=-1, keepdim=True) / 7.0
            q_out = torch.clamp(torch.round(blocked_out / scale_out), -7, 7)
            ffn_out = (q_out * scale_out).view(ffn_out.shape)
            
        x = residual + ffn_out
        
        sqnr = measure_sqnr(baseline_output, x)
        results.append({"Experiment": exp["name"], "SQNR (dB)": round(sqnr, 2)})
        
    df = pd.DataFrame(results)
    print("\n" + df.to_markdown(index=False))

if __name__ == "__main__":
    run_lut_ablation()
