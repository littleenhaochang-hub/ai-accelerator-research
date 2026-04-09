import torch
import torch.nn as nn
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

# --- Core Quantization ---
NF4_LUT = torch.tensor([-1.0, -0.6961928, -0.5250731, -0.3949175, -0.2844414, -0.1847734, -0.0910500, 0.0, 0.0795803, 0.1609302, 0.2461123, 0.3379152, 0.4407098, 0.5626170, 0.7229568, 1.0])

def e8m0_scale(amax): return 2.0 ** torch.round(torch.log2(amax.clamp(min=1e-7)))

def fake_quant_pertensor(x, bits=8):
    amax = torch.amax(torch.abs(x)).clamp(min=1e-7)
    scale = amax / ((2**(bits-1)) - 1)
    q = torch.clamp(torch.round(x / scale), -(2**(bits-1)), (2**(bits-1)) - 1)
    return q * scale

def fake_quant_subchannel(x, bits=8, block_size=128):
    orig_shape = x.shape
    pad_len = (block_size - orig_shape[-1] % block_size) % block_size
    if pad_len > 0: x = torch.nn.functional.pad(x, (0, pad_len))
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True)
    scale = e8m0_scale(amax / ((2**(bits-1)) - 1))
    q = torch.clamp(torch.round(x_blocked / scale), -(2**(bits-1)), (2**(bits-1)) - 1)
    dq = (q * scale).view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else (q * scale).view(orig_shape)
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
    indices = torch.argmin(torch.abs(x_scaled.unsqueeze(-1) - lut), dim=-1)
    dq = (lut[indices] * amax).view(orig_shape[0], orig_shape[1], -1) if len(orig_shape) == 3 else (lut[indices] * amax).view(orig_shape)
    if pad_len > 0: dq = dq[..., :-pad_len]
    return dq

def simulate_chained_householder(x, num_reflections=4):
    orig_shape = x.shape
    if len(orig_shape) == 3: B, Seq, H = orig_shape; x_reshaped = x.view(-1, H)
    else: H = orig_shape[-1]; x_reshaped = x.view(-1, H)
    torch.manual_seed(42)
    for _ in range(num_reflections):
        v = torch.randn(H, device=x.device, dtype=x.dtype)
        v = v / torch.norm(v)
        x_reshaped = x_reshaped - 2 * torch.matmul(x_reshaped, v.unsqueeze(1)) * v.unsqueeze(0)
    return x_reshaped.view(orig_shape)

# --- Core Accumulator ---
def float_to_fp24(tensor, mode="round"):
    t_int = tensor.view(torch.int32)
    if mode == "round": t_int = t_int + 0x00000080
    t_int = t_int & 0xFFFFFF00
    return t_int.view(torch.float32)

def parallel_fp24_linear(A, W, bias=None, chunk_size=32, mode="round"):
    orig_shape = A.shape
    A_flat = A.view(-1, A.shape[-1])
    N, In_Dim = A_flat.shape
    Out_Dim = W.shape[0]

    pad_len = (chunk_size - In_Dim % chunk_size) % chunk_size
    if pad_len > 0:
        A_flat = torch.nn.functional.pad(A_flat, (0, pad_len))
        W = torch.nn.functional.pad(W, (0, pad_len))
        In_Dim += pad_len

    K_chunks = In_Dim // chunk_size
    A_c = A_flat.view(N, K_chunks, chunk_size)
    W_c = W.view(Out_Dim, K_chunks, chunk_size)
    
    partials = torch.einsum('nkc,okc->nko', A_c, W_c)
    acc = torch.zeros((N, Out_Dim), device=A.device, dtype=torch.float32)
    
    for i in range(K_chunks):
        acc = acc + partials[:, i, :]
        acc = float_to_fp24(acc, mode=mode)
        
    if bias is not None:
        acc = acc + bias
        acc = float_to_fp24(acc, mode=mode)
        
    out_shape = list(orig_shape[:-1]) + [Out_Dim]
    return acc.view(out_shape)

# --- Module Wrapper ---
class HardwareSimWrapper(nn.Module):
    def __init__(self, orig_linear, config):
        super().__init__()
        self.weight = orig_linear.weight
        self.bias = orig_linear.bias
        self.config = config
        
    def _quantize(self, x, is_weight=False):
        c = self.config
        bits = c["w_bit"] if is_weight else c["a_bit"]
        if bits == 16: return x
        
        if c["type"] == "pertensor":
            return fake_quant_pertensor(x, bits=bits)
        elif c["type"] == "subchannel":
            return fake_quant_subchannel(x, bits=bits, block_size=128)
        elif c["type"] == "lut_turbo":
            if is_weight:
                return fake_quant_nf4_lut(x, block_size=128)
            else:
                smeared = simulate_chained_householder(x)
                fq = fake_quant_nf4_lut(smeared, block_size=128)
                return simulate_chained_householder(fq)
        return x
        
    def forward(self, x):
        # 1. Fake Quantize X and W
        x_q = self._quantize(x, is_weight=False)
        w_q = self._quantize(self.weight, is_weight=True)
        
        # 2. Accumulate in FP24 or FP32
        if self.config["acc_fp24"]:
            out_f32 = parallel_fp24_linear(x_q.float(), w_q.float(), self.bias.float() if self.bias is not None else None, chunk_size=32, mode="round")
            return out_f32.to(x.dtype)
        else:
            return torch.nn.functional.linear(x_q, w_q, self.bias)

def replace_model_layers(model, config):
    for layer in model.model.layers:
        layer.self_attn.q_proj = HardwareSimWrapper(layer.self_attn.q_proj, config)
        layer.self_attn.k_proj = HardwareSimWrapper(layer.self_attn.k_proj, config)
        layer.self_attn.v_proj = HardwareSimWrapper(layer.self_attn.v_proj, config)
        layer.self_attn.o_proj = HardwareSimWrapper(layer.self_attn.o_proj, config)
        layer.mlp.gate_proj = HardwareSimWrapper(layer.mlp.gate_proj, config)
        layer.mlp.up_proj = HardwareSimWrapper(layer.mlp.up_proj, config)
        layer.mlp.down_proj = HardwareSimWrapper(layer.mlp.down_proj, config)

def evaluate_ppl(model, tokenizer, texts, seq_len=1024, max_tokens=2048):
    text = "\n\n".join(texts)
    encodings = tokenizer(text, return_tensors="pt")
    nlls = []
    total_len = min(encodings.input_ids.size(1), max_tokens)
    samples_to_run = total_len // seq_len
    for i in range(samples_to_run):
        begin_loc = i * seq_len
        end_loc = begin_loc + seq_len
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(model.device)
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            nlls.append(outputs.loss)
    if len(nlls) == 0: return float('inf')
    return torch.exp(torch.stack(nlls).mean()).item()

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print("Loading Baseline Model and Datasets...")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
    
    ds_wiki = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
    ds_ptb = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="validation")
    
    # We use a small token slice (2048 tokens) to finish the dense 5x2 grid quickly
    texts_wiki = ds_wiki["text"][:1000]
    texts_ptb = ds_ptb["text"][:1000]

    configs = [
        {"name": "1. W16_A16 + FP32 Acc", "w_bit": 16, "a_bit": 16, "type": "none", "acc_fp24": False},
        {"name": "2. W8_A8 (PerTensor) + FP24 Acc", "w_bit": 8, "a_bit": 8, "type": "pertensor", "acc_fp24": True},
        {"name": "3. W8_A8 (SubCh B128) + FP24 Acc", "w_bit": 8, "a_bit": 8, "type": "subchannel", "acc_fp24": True},
        {"name": "4. W4_A4 (Linear B128) + FP24 Acc", "w_bit": 4, "a_bit": 4, "type": "subchannel", "acc_fp24": True},
        {"name": "5. W4_A4 (LUT+Turbo) + FP24 Acc", "w_bit": 4, "a_bit": 4, "type": "lut_turbo", "acc_fp24": True},
    ]

    results = []
    
    for c in configs:
        print(f"\nEvaluating: {c['name']}")
        model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
        if c["type"] != "none" or c["acc_fp24"]:
            replace_model_layers(model, c)
            
        print("  -> Running WikiText-2...")
        ppl_wiki = evaluate_ppl(model, tokenizer, texts_wiki, seq_len=1024, max_tokens=2048)
        print(f"     PPL: {ppl_wiki:.3f}")
        
        print("  -> Running Penn Treebank (PTB)...")
        ppl_ptb = evaluate_ppl(model, tokenizer, texts_ptb, seq_len=1024, max_tokens=2048)
        print(f"     PPL: {ppl_ptb:.3f}")
        
        results.append({
            "Architecture / Config": c["name"],
            "WikiText-2 PPL": round(ppl_wiki, 3),
            "PTB PPL": round(ppl_ptb, 3)
        })
        
        del model # free memory
        torch.mps.empty_cache() if device == "mps" else torch.cuda.empty_cache()

    df = pd.DataFrame(results)
    print("\n" + "="*80)
    print("UNIVERSAL BENCHMARK (COMPOUND NOISE EVALUATION)")
    print("="*80)
    print(df.to_markdown(index=False))

if __name__ == "__main__":
    main()
