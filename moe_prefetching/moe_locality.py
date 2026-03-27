import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen1.5-MoE-A2.7B"
print(f"Loading {model_id} (small MoE for fast testing)...")

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    trust_remote_code=True
)

prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. This is why DRAM-less SSDs are cheaper but significantly slower for random I/O operations."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

seq_len = inputs.input_ids.shape[1]
print(f"Input sequence length: {seq_len} tokens")

with torch.no_grad():
    outputs = model(**inputs, output_router_logits=True, return_dict=True)

# router_logits is a tuple of length num_moe_layers
router_logits = outputs.router_logits
layer_idx = len(router_logits) // 2
logits = router_logits[layer_idx]

probs = torch.nn.functional.softmax(logits, dim=-1)
# Qwen1.5-MoE-A2.7B has 60 experts, routes to 4
top_k_probs, top_k_indices = torch.topk(probs, k=4, dim=-1)

experts_used = set()
for i in range(len(top_k_indices)):
    experts_used.update(top_k_indices[i].tolist())
    
print(f"\n--- Locality Analysis (Layer {layer_idx}) ---")
print(f"Total unique experts activated across {seq_len} tokens: {len(experts_used)} / 60")

# Simulate a DRAM cache of size 8
cache_size = 8
cache = []
hits = 0
misses = 0

for i in range(len(top_k_indices)):
    req_experts = top_k_indices[i].tolist()
    for exp in req_experts:
        if exp in cache:
            hits += 1
            cache.remove(exp) # LRU
            cache.append(exp)
        else:
            misses += 1
            if len(cache) >= cache_size:
                cache.pop(0)
            cache.append(exp)
            
hit_rate = hits / (hits + misses)
print(f"SSD-to-DRAM prefetch simulation (Cache Size = {cache_size} experts)")
print(f"Hit Rate: {hit_rate*100:.2f}%")
