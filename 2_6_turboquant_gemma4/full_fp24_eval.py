import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

def float_to_fp24(tensor, mode="round"):
    t_int = tensor.view(torch.int32)
    if mode == "round":
        t_int = t_int + 0x00000080
    t_int = t_int & 0xFFFFFF00
    return t_int.view(torch.float32)

def parallel_fp24_linear(A, W, bias=None, chunk_size=32, mode="round"):
    # Reshape manually to support varying batch/seq dims cleanly
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
    
    # We want partials of shape: [N, K_chunks, Out_Dim]
    # A_c: [N, K_chunks, chunk_size] -> unsqueeze(2) -> [N, K_chunks, 1, chunk_size]
    # W_c: [Out_Dim, K_chunks, chunk_size] -> transpose/unsqueeze -> [1, K_chunks, chunk_size, Out_Dim]
    # Actually, standard bmm or einsum is safest. Let's use einsum.
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

class FP24LinearWrapper(nn.Module):
    def __init__(self, orig_linear, chunk_size=32, mode="round"):
        super().__init__()
        self.weight = orig_linear.weight
        self.bias = orig_linear.bias
        self.chunk_size = chunk_size
        self.mode = mode
        
    def forward(self, x):
        x_f32 = x.float()
        w_f32 = self.weight.float()
        b_f32 = self.bias.float() if self.bias is not None else None
        out_f32 = parallel_fp24_linear(x_f32, w_f32, b_f32, self.chunk_size, self.mode)
        return out_f32.to(x.dtype)

def replace_with_fp24(model, chunk_size=32, mode="round"):
    print(f"Injecting FP24 (Chunk={chunk_size}, Mode={mode}) into ALL Linear Layers...")
    replaced_count = 0
    for layer in model.model.layers:
        layer.self_attn.q_proj = FP24LinearWrapper(layer.self_attn.q_proj, chunk_size, mode)
        layer.self_attn.k_proj = FP24LinearWrapper(layer.self_attn.k_proj, chunk_size, mode)
        layer.self_attn.v_proj = FP24LinearWrapper(layer.self_attn.v_proj, chunk_size, mode)
        layer.self_attn.o_proj = FP24LinearWrapper(layer.self_attn.o_proj, chunk_size, mode)
        layer.mlp.gate_proj = FP24LinearWrapper(layer.mlp.gate_proj, chunk_size, mode)
        layer.mlp.up_proj = FP24LinearWrapper(layer.mlp.up_proj, chunk_size, mode)
        layer.mlp.down_proj = FP24LinearWrapper(layer.mlp.down_proj, chunk_size, mode)
        replaced_count += 7
    print(f"Replaced {replaced_count} linear layers.")

def evaluate_ppl(model, tokenizer, dataset, seq_len=1024, max_tokens=10000):
    text = "\n\n".join(dataset["text"][:2000])
    encodings = tokenizer(text, return_tensors="pt")
    nlls = []
    total_len = min(encodings.input_ids.size(1), max_tokens)
    samples_to_run = total_len // seq_len
    
    print(f"Evaluating PPL over {samples_to_run * seq_len} tokens...")
    for i in tqdm(range(samples_to_run), desc="PPL Evaluation"):
        begin_loc = i * seq_len
        end_loc = begin_loc + seq_len
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(model.device)
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            nlls.append(outputs.loss)
    return torch.exp(torch.stack(nlls).mean()).item()

def run_experiment():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print("Loading Baseline Model...")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
    model_fp32 = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
    
    prompt = "The architecture of a neural network accelerator heavily relies on"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    print("\n================== BASELINE (FP32 ACC) ==================")
    ppl_fp32 = evaluate_ppl(model_fp32, tokenizer, dataset, max_tokens=2048)
    print(f"Baseline PPL: {ppl_fp32:.3f}")
    
    with torch.no_grad():
        out_fp32 = model_fp32.generate(**inputs, max_new_tokens=40, do_sample=False)
        text_fp32 = tokenizer.decode(out_fp32[0], skip_special_tokens=True)
    print(f"\n[Qualitative Output - FP32]:\n{text_fp32}")
    
    print("\n================== FP24 ACCUMULATOR ==================")
    model_fp24 = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    replace_with_fp24(model_fp24, chunk_size=32, mode="round")
    
    ppl_fp24 = evaluate_ppl(model_fp24, tokenizer, dataset, max_tokens=2048)
    print(f"FP24 PPL: {ppl_fp24:.3f}")
    
    with torch.no_grad():
        out_fp24 = model_fp24.generate(**inputs, max_new_tokens=40, do_sample=False)
        text_fp24 = tokenizer.decode(out_fp24[0], skip_special_tokens=True)
    print(f"\n[Qualitative Output - FP24]:\n{text_fp24}")
    
    print("\n================== SUMMARY ==================")
    print(f"FP32 Baseline PPL : {ppl_fp32:.3f}")
    print(f"FP24 (Chunk 32) PPL: {ppl_fp24:.3f}")
    delta = ppl_fp24 - ppl_fp32
    print(f"PPL Degradation    : +{delta:.3f}")
    match = "MATCH" if text_fp32 == text_fp24 else "DIVERGED"
    print(f"Qualitative Text   : {match}")

if __name__ == "__main__":
    run_experiment()
