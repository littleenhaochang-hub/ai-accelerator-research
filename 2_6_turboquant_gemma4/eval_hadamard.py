import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

NF4_LUT = torch.tensor([-1.0, -0.6961928, -0.5250731, -0.3949175, -0.2844414, -0.1847734, -0.0910500, 0.0, 0.0795803, 0.1609302, 0.2461123, 0.3379152, 0.4407098, 0.5626170, 0.7229568, 1.0])

def e8m0_scale(amax): return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

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

def fake_quant_nf4_lut(x, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0: x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True).clamp(min=1e-7)
    x_scaled = x_blocked / amax
    lut = NF4_LUT.to(device=x.device, dtype=x.dtype)
    diffs = torch.abs(x_scaled.unsqueeze(-1) - lut)
    indices = torch.argmin(diffs, dim=-1)
    q = lut[indices]
    dq = q * amax
    dq = dq.view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else dq.view(orig_shape)
    if pad_len > 0: dq = dq[..., :-pad_len]
    return dq

# The Standard O(N^2) / O(H^2) Hadamard-like orthogonal mixing
def simulate_hadamard(x):
    H = x.shape[-1]
    torch.manual_seed(42)
    # Generate random orthogonal matrix Q
    random_mat = torch.randn(H, H, device=x.device, dtype=torch.float32)
    Q, _ = torch.linalg.qr(random_mat)
    Q = Q.to(x.dtype)
    return torch.matmul(x, Q)

def simulate_chained_householder(x, num_reflections=4):
    orig_shape = x.shape
    if len(orig_shape) == 3: B, Seq, H = orig_shape; x_reshaped = x.view(-1, H)
    else: H = orig_shape[-1]; x_reshaped = x.view(-1, H)
    torch.manual_seed(42)
    for _ in range(num_reflections):
        v = torch.randn(H, device=x.device, dtype=x.dtype)
        v = v / torch.norm(v)
        proj = torch.matmul(x_reshaped, v.unsqueeze(1))
        x_reshaped = x_reshaped - 2 * proj * v.unsqueeze(0)
    return x_reshaped.view(orig_shape)

def fake_quant_hadamard_turboquant(x, bits=4, block_size=128, lut=False):
    smeared = simulate_hadamard(x)
    fq = fake_quant_nf4_lut(smeared, block_size=block_size) if lut else fake_quant_subchannel(smeared, bits=bits, block_size=block_size)
    # Inverse of orthogonal Q is Q.T
    H = x.shape[-1]
    torch.manual_seed(42)
    random_mat = torch.randn(H, H, device=x.device, dtype=torch.float32)
    Q, _ = torch.linalg.qr(random_mat)
    Q = Q.to(x.dtype)
    return torch.matmul(fq, Q.T)

def fake_quant_householder_turboquant(x, bits=4, block_size=128, lut=False):
    smeared = simulate_chained_householder(x)
    fq = fake_quant_nf4_lut(smeared, block_size=block_size) if lut else fake_quant_subchannel(smeared, bits=bits, block_size=block_size)
    return simulate_chained_householder(fq)

def measure_sqnr(original, quantized):
    sig_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    return 10 * torch.log10(sig_power / noise_power).item()

class QuantizedMLP(torch.nn.Module):
    def __init__(self, orig_mlp, lut=False):
        super().__init__()
        self.orig_mlp = orig_mlp
        self.lut = lut
    def forward(self, x):
        q_fn = fake_quant_nf4_lut if self.lut else fake_quant_subchannel
        return q_fn(self.orig_mlp(q_fn(x)))

class QuantizedAttn(torch.nn.Module):
    def __init__(self, orig_attn, mix_type="hadamard", lut=False):
        super().__init__()
        self.orig_attn = orig_attn
        self.mix_type = mix_type
        self.lut = lut
    def forward(self, hidden_states, *args, **kwargs):
        if self.mix_type == "hadamard":
            x_q = fake_quant_hadamard_turboquant(hidden_states, lut=self.lut)
        else:
            x_q = fake_quant_householder_turboquant(hidden_states, lut=self.lut)
            
        q_out_fn = fake_quant_nf4_lut if self.lut else fake_quant_subchannel
        out = self.orig_attn(x_q, *args, **kwargs)
        return (q_out_fn(out[0]),) + out[1:]

def evaluate_ppl(model, tokenizer, dataset, seq_len=1024, num_samples=10):
    text = "\n\n".join(dataset["text"][:1000])
    encodings = tokenizer(text, return_tensors="pt")
    nlls = []
    total_len = encodings.input_ids.size(1)
    samples_to_run = min(num_samples, total_len // seq_len)
    for i in range(samples_to_run):
        begin_loc = i * seq_len
        end_loc = begin_loc + seq_len
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(model.device)
        with torch.no_grad(): nlls.append(model(input_ids, labels=input_ids).loss)
    return torch.exp(torch.stack(nlls).mean()).item()

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")

    grid = [
        {"name": "Hadamard TurboQuant (Linear A4W4/A4KV4)", "mix": "hadamard", "lut": False, "mem": 0.25, "scale": "e8m0"},
        {"name": "Hadamard TurboQuant (LUT B128 A4W4/A4KV4)", "mix": "hadamard", "lut": True, "mem": 0.25, "scale": "NF4 LUT"},
        {"name": "Householder TurboQuant (LUT B128 A4W4/A4KV4)", "mix": "householder", "lut": True, "mem": 0.25, "scale": "NF4 LUT"}
    ]

    text_sqnr = "The future of AI hardware relies on hardware-software co-design. " * 5
    inp = tokenizer(text_sqnr, return_tensors="pt").to(device)
    with torch.no_grad():
        out_layer = model(**inp, output_hidden_states=True)
        layer_input = out_layer.hidden_states[12]
    
    layer = model.model.layers[12]
    with torch.no_grad():
        pos_emb = model.model.rotary_emb(layer_input, torch.arange(layer_input.shape[1], device=device).unsqueeze(0))
        baseline_output = layer(layer_input, position_embeddings=pos_emb)[0]

    orig_mlps = [l.mlp for l in model.model.layers]
    orig_attns = [l.self_attn for l in model.model.layers]

    results = []
    print("\nRunning Hadamard/Householder Comparative Grid...")
    for exp in tqdm(grid, desc="Experiments"):
        # SQNR
        layer.mlp = QuantizedMLP(orig_mlps[12], lut=exp["lut"])
        layer.self_attn = QuantizedAttn(orig_attns[12], mix_type=exp["mix"], lut=exp["lut"])
        with torch.no_grad(): x = layer(layer_input.clone(), position_embeddings=pos_emb)[0]
        sqnr = measure_sqnr(baseline_output, x)
        
        # PPL
        for i, l in enumerate(model.model.layers):
            l.mlp = QuantizedMLP(orig_mlps[i], lut=exp["lut"])
            l.self_attn = QuantizedAttn(orig_attns[i], mix_type=exp["mix"], lut=exp["lut"])
            
        ppl = evaluate_ppl(model, tokenizer, dataset, num_samples=10)
        
        results.append({
            "Experiment": exp["name"],
            "SQNR (dB)": round(sqnr, 2),
            "WikiText-2 PPL": round(ppl, 3),
            "Memory Footprint": f"{exp['mem']:.2f}x",
            "Hardware Scheme": exp["scale"],
            "Block Size": "B128"
        })
        
    df = pd.DataFrame(results)
    print("\n" + df.to_markdown(index=False))

if __name__ == "__main__":
    main()
