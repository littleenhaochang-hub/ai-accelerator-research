import torch
import torch.nn as nn
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import collections

# We will simulate an MoE router using a dense model's intermediate features.
# Since we don't have a small MoE model on hand, we will use Qwen-0.5B's FFN activations 
# to train a lightweight K-Means or GMM (simulating a Router) to prove that consecutive tokens
# get routed to the same "Expert Cluster" (Temporal Locality).

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def simulate_moe_routing(hidden_states, num_experts=8, top_k=2):
    """
    Simulates MoE routing by clustering the hidden states.
    We use a random projection matrix as a fixed "Router" for this simulation.
    """
    bsz, seq_len, hidden_dim = hidden_states.shape
    
    # Create a fixed pseudo-router
    torch.manual_seed(42)
    router_weights = torch.randn(hidden_dim, num_experts, device=hidden_states.device, dtype=hidden_states.dtype)
    
    # Calculate routing logits
    logits = torch.matmul(hidden_states.view(-1, hidden_dim), router_weights)
    
    # Get top-k experts for each token
    routing_probs = torch.softmax(logits, dim=-1)
    _, selected_experts = torch.topk(routing_probs, top_k, dim=-1)
    
    return selected_experts.view(bsz, seq_len, top_k)

def calculate_locality_metrics(selected_experts):
    """
    Calculates Temporal Locality: How often does token T+1 use the SAME expert as token T?
    """
    bsz, seq_len, top_k = selected_experts.shape
    
    hits = 0
    total_transitions = 0
    
    # Track cache state (simulating an SRAM buffer that holds 'cache_size' experts)
    # Let's say SRAM can hold 2 experts at a time.
    sram_cache = set()
    sram_hits = 0
    sram_misses = 0
    
    for i in range(seq_len - 1):
        current_experts = set(selected_experts[0, i].tolist())
        next_experts = set(selected_experts[0, i+1].tolist())
        
        # Immediate temporal locality (T to T+1 overlap)
        if len(current_experts.intersection(next_experts)) > 0:
            hits += 1
        total_transitions += 1
        
        # SRAM Simulation (LRU or simple greedy)
        # Update cache with current experts
        for exp in current_experts:
            sram_cache.add(exp)
        if len(sram_cache) > 3: # Cache capacity = 3 experts
            # Remove a random one not in current_experts (FIFO/LRU simulation)
            for item in list(sram_cache):
                if item not in current_experts:
                    sram_cache.remove(item)
                    break
        
        # If cache exceeds capacity (e.g., 2), we simulate a miss for new ones
        # For simplicity, let's just track if the next expert was already in the current working set
        for n_exp in next_experts:
            if n_exp in sram_cache:
                sram_hits += 1
            else:
                sram_misses += 1

    immediate_locality = (hits / total_transitions) * 100 if total_transitions > 0 else 0
    cache_hit_rate = (sram_hits / (sram_hits + sram_misses)) * 100 if (sram_hits + sram_misses) > 0 else 0
    
    return immediate_locality, cache_hit_rate

def run():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    
    # Test texts with different contextual shifts
    texts = [
        "The quick brown fox jumps over the lazy dog. It is a very sunny day.", # Pure English narrative
        "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)", # Pure Python
        "Here is a Python function to calculate Fibonacci:\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\nThis function uses recursion.", # Context Switch (Eng -> Code -> Eng)
    ]
    
    print("--- Simulating MoE Drafter Router Locality (8 Experts, Top-1 Routing) ---")
    
    for i, text in enumerate(texts):
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)
            
        # We check the routing behavior at a middle layer (e.g., layer 12)
        mid_layer_hidden = outputs.hidden_states[12]
        
        # Simulate routing (Top-1 for extreme memory saving)
        selected_experts = simulate_moe_routing(mid_layer_hidden, num_experts=8, top_k=2)
        
        imm_loc, hit_rate = calculate_locality_metrics(selected_experts)
        
        print(f"\nScenario {i+1}: {text[:40]}...")
        print(f"Token Count: {inputs.input_ids.shape[1]}")
        print(f"T->T+1 Expert Overlap (Temporal Locality): {imm_loc:.1f}%")
        print(f"SRAM Expert Hit Rate (Assuming 1 Active Slot): {hit_rate:.1f}%")
        
        # Print the actual routing sequence to visualize it
        route_seq = selected_experts[0, :, 0].tolist()
        print(f"Routing Sequence: {route_seq}")

if __name__ == "__main__":
    run()
