import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

def e8m0_scale(amax):
    return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

def fake_quant_subchannel(x, bits=4, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0: x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True)
    scale = e8m0_scale(amax / ((2**(bits-1)) - 1))
    q = torch.round(x_blocked / scale)
    q = torch.clamp(q, -(2**(bits-1)), (2**(bits-1)) - 1)
    dq = q * scale
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0: dq = dq[..., :-pad_len]
    return dq

def generate_random_orthogonal(dim, device, dtype):
    """Generates a random orthogonal matrix (Q from QR decomposition)"""
    torch.manual_seed(42)
    random_mat = torch.randn(dim, dim, device=device, dtype=torch.float32)
    Q, _ = torch.linalg.qr(random_mat)
    return Q.to(dtype)

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

def run_spinquant_prototype():
    print("Initiating Auto-Researcher Prototype: FFN Outlier Rotation (SpinQuant concept)")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    
    text = "The future of AI hardware relies on mitigating severe activation outliers in the feed-forward network to enable extreme 4-bit quantization without performance collapse. " * 5
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        # Extract Layer 12 input to FFN
        layer = model.model.layers[12]
        x_in = layer.post_attention_layernorm(outputs.hidden_states[12].float())
        
        # Real baseline FFN output
        gate_up = layer.mlp.act_fn(layer.mlp.gate_proj(x_in)) * layer.mlp.up_proj(x_in)
        baseline_out = layer.mlp.down_proj(gate_up)
    
    print("\n--- Phase 1: Naive A4W4 FFN (Subchannel) ---")
    x_in_q = fake_quant_subchannel(x_in, bits=4)
    w_gate_q = fake_quant_subchannel(layer.mlp.gate_proj.weight.float(), bits=4)
    w_up_q = fake_quant_subchannel(layer.mlp.up_proj.weight.float(), bits=4)
    w_down_q = fake_quant_subchannel(layer.mlp.down_proj.weight.float(), bits=4)
    
    # Naive forward
    gate_up_q = layer.mlp.act_fn(torch.nn.functional.linear(x_in_q, w_gate_q)) * torch.nn.functional.linear(x_in_q, w_up_q)
    gate_up_q_a4 = fake_quant_subchannel(gate_up_q, bits=4) # quantize activation before down_proj
    naive_out = torch.nn.functional.linear(gate_up_q_a4, w_down_q)
    sqnr_naive = measure_sqnr(baseline_out, naive_out)
    print(f"Naive A4W4 SQNR: {sqnr_naive:.2f} dB (Severe Outlier Clipping)")
    
    print("\n--- Phase 2: Rotation-based Smoothing (SpinQuant/QuaRot concept) ---")
    # We apply an orthogonal rotation matrix R to the input of down_proj to "smear" outliers
    hidden_dim = gate_up.shape[-1]
    R = generate_random_orthogonal(hidden_dim, device=x_in.device, dtype=torch.float32)
    
    # Rotate the activations (X * R)
    gate_up_rotated = torch.matmul(gate_up_q, R)
    # Quantize the rotated activations (now smoothed, outliers destroyed)
    gate_up_rotated_a4 = fake_quant_subchannel(gate_up_rotated, bits=4)
    
    # Rotate the weights (W * R)
    # y = (X * R) * (W * R)^T = X * R * R^T * W^T = X * W^T
    w_down_rotated = torch.matmul(layer.mlp.down_proj.weight.float(), R)
    w_down_rotated_w4 = fake_quant_subchannel(w_down_rotated, bits=4)
    
    rotated_out = torch.nn.functional.linear(gate_up_rotated_a4, w_down_rotated_w4)
    sqnr_rotated = measure_sqnr(baseline_out, rotated_out)
    
    print(f"Rotated A4W4 SQNR: {sqnr_rotated:.2f} dB")
    print(f"Improvement: +{sqnr_rotated - sqnr_naive:.2f} dB")

if __name__ == "__main__":
    run_spinquant_prototype()
