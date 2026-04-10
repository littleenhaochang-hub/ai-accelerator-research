import torch
import collections
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

MODEL_ID = "Qwen/Qwen1.5-MoE-A2.7B"

# Global dictionary to store expert selection frequencies
# format: layer_idx -> expert_idx -> count
expert_hit_counts = collections.defaultdict(lambda: collections.defaultdict(int))

def make_router_hook(layer_idx, num_experts_per_tok):
    def hook(module, input, output):
        # output is the router logits: [batch, seq_len, num_experts]
        logits = output.detach().cpu().float()
        
        # Calculate top-k experts selected by the router
        _, selected_experts = torch.topk(logits, k=num_experts_per_tok, dim=-1)
        
        # Flatten and count
        selected_experts = selected_experts.view(-1).numpy()
        for exp_id in selected_experts:
            expert_hit_counts[layer_idx][exp_id] += 1
            
    return hook

def run_profiler():
    print(f"Loading {MODEL_ID} (This might take a minute)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # Load model (we can use CPU or MPS, using CPU for reliability during profiling since we only need the router logits)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        torch_dtype=torch.float16, 
        device_map="cpu"
    )
    
    config = model.config
    num_routed_experts = getattr(config, "num_experts", 60)
    num_experts_per_tok = getattr(config, "num_experts_per_tok", 4)
    
    print(f"\n[Model Architecture]")
    print(f"Total Routed Experts: {num_routed_experts}")
    print(f"Experts Selected per Token: {num_experts_per_tok}")
    
    # Register Hooks on all MoE Routers
    hook_count = 0
    for i, layer in enumerate(model.model.layers):
        # Qwen MoE uses `mlp.gate` as the router
        if hasattr(layer.mlp, "gate"):
            layer.mlp.gate.register_forward_hook(make_router_hook(i, num_experts_per_tok))
            hook_count += 1
            
    print(f"Registered {hook_count} router hooks.")
    
    # Prepare a diverse corpus for realistic profiling
    test_text = """
    Artificial intelligence is a rapidly evolving field. In recent years, Large Language Models (LLMs) like GPT-4, Llama, and Qwen have demonstrated remarkable capabilities in natural language understanding, reasoning, and coding. 
    To optimize these models for edge devices, engineers use quantization (such as W4A4) and Mixture of Experts (MoE) architectures. 
    MoE reduces active parameters by routing tokens to specific experts.
    Here is a simple Python function to calculate the Fibonacci sequence:
    def fibonacci(n):
        if n <= 0: return 0
        elif n == 1: return 1
        return fibonacci(n-1) + fibonacci(n-2)
    The universe is vast and full of mysteries. Black holes, quantum mechanics, and the theory of relativity continue to puzzle scientists.
    """
    
    inputs = tokenizer(test_text, return_tensors="pt").to(model.device)
    total_tokens = inputs.input_ids.shape[1]
    print(f"\nProcessing {total_tokens} tokens to extract Real Expert Traces...")
    
    with torch.no_grad():
        model(inputs.input_ids)
        
    print("\n=== Real Expert Hit Rate Analysis (Expert Pinning) ===")
    
    # We will analyze the middle layer (often the most representative)
    middle_layer = hook_count // 2
    
    for layer_idx in [1, middle_layer, hook_count - 2]:
        counts = expert_hit_counts[layer_idx]
        total_hits = sum(counts.values())
        
        # Sort experts by frequency
        sorted_experts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate how many experts represent the top 25% of the capacity
        top_25_percent_capacity = max(1, num_routed_experts // 4)
        
        hits_in_top_25 = sum(count for exp_id, count in sorted_experts[:top_25_percent_capacity])
        pinning_hit_rate = (hits_in_top_25 / total_hits) * 100 if total_hits > 0 else 0
        
        print(f"\nLayer {layer_idx}:")
        print(f"  Total Routing Decisions: {total_hits}")
        print(f"  Top {top_25_percent_capacity} Experts (25% capacity) Hit Rate: {pinning_hit_rate:.1f}%")
        
        # Show the most popular experts
        top_3 = [(exp, count, count/total_hits*100) for exp, count in sorted_experts[:3]]
        print(f"  Top 3 Hottest Experts: " + ", ".join([f"E{exp} ({pct:.1f}%)" for exp, count, pct in top_3]))
        
        # Show the coldest experts (dead weight)
        coldest = [(exp, count) for exp, count in sorted_experts[-3:]]
        print(f"  Coldest Experts: " + ", ".join([f"E{exp} ({count} hits)" for exp, count in coldest]))

run_profiler()
