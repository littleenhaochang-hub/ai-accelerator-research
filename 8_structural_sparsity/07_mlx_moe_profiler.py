import sys
import collections
import numpy as np

try:
    import mlx.core as mx
    from mlx_lm import load, generate
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

MODEL_ID = "Qwen/Qwen1.5-MoE-A2.7B"
print(f"Loading {MODEL_ID} via Apple MLX Unified Memory (mmap)...")

try:
    model, tokenizer = load(MODEL_ID)
except Exception as e:
    print(f"Failed to load model in MLX: {e}")
    sys.exit(1)

print("Model loaded successfully! Patching MLX MoE Routers...")

expert_hits = collections.defaultdict(lambda: collections.defaultdict(int))

def get_patch_gate(orig_gate, layer_idx):
    def new_gate(x):
        logits = orig_gate(x)
        # Qwen MoE uses top-k=4
        top_k = 4
        # Since MLX operations are lazy graphs, we must evaluate them to read values
        scores, indices = mx.topk(logits, k=top_k, axis=-1)
        mx.eval(indices)
        idx_list = indices.flatten().tolist()
        for val in idx_list:
            expert_hits[layer_idx][val] += 1
        return logits
    return new_gate

# Apply monkey-patch to MLX model layers
patched_count = 0
for i, layer in enumerate(model.model.layers):
    if hasattr(layer, "mlp") and hasattr(layer.mlp, "gate"):
        layer.mlp.gate = get_patch_gate(layer.mlp.gate, i)
        patched_count += 1

print(f"Patched {patched_count} routers. Processing tokens...")

prompt = """
Artificial intelligence is a rapidly evolving field. In recent years, Large Language Models (LLMs) like GPT-4, Llama, and Qwen have demonstrated remarkable capabilities in natural language understanding, reasoning, and coding. 
To optimize these models for edge devices, engineers use quantization (such as W4A4) and Mixture of Experts (MoE) architectures. 
Here is a simple Python function to calculate the Fibonacci sequence:
def fibonacci(n):
    if n <= 0: return 0
    elif n == 1: return 1
    return fibonacci(n-1) + fibonacci(n-2)
"""

_ = generate(model, tokenizer, prompt=prompt, max_tokens=1, verbose=False)

print("\n=== Real Expert Hit Rate Analysis (Apple MLX Profiler) ===")
for layer_idx in sorted(expert_hits.keys()):
    counts = expert_hits[layer_idx]
    if not counts: continue
    total = sum(counts.values())
    sorted_exp = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    # Qwen1.5-MoE-A2.7B has 60 routed experts
    top_25_pct = 15 
    hits_top_15 = sum(c for e, c in sorted_exp[:top_25_pct])
    
    print(f"\nLayer {layer_idx:02d} | Routing Requests: {total}")
    print(f"  Top 25% Experts (15/60) Hit Rate: {hits_top_15/total*100:.1f}%")
    top_3 = ", ".join([f"E{e} ({c/total*100:.1f}%)" for e, c in sorted_exp[:3]])
    print(f"  Hottest Experts: {top_3}")
    
    zeros = 60 - len(sorted_exp)
    print(f"  Cold Experts (0 hits): {zeros}/60")

