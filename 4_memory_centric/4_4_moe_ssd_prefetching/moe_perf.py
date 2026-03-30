import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen1.5-MoE-A2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. This is why DRAM-less SSDs are cheaper but significantly slower for random I/O operations."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model(**inputs, output_router_logits=True, return_dict=True)

logits = outputs.router_logits[12] # Layer 12
probs = torch.nn.functional.softmax(logits, dim=-1)
_, top_k_indices = torch.topk(probs, k=4, dim=-1)

# HW Assumptions
EXPERT_SIZE_MB = 32 # Approx size of one expert in this model
DRAM_BW_GBPS = 95.0
SSD_BW_GBPS = 10.0

print(f"\n--- MoE Prefetch Performance Simulation (Layer 12) ---")
print(f"Sequence Length: {inputs.input_ids.shape[1]} tokens")
print(f"Assumed Expert Size: {EXPERT_SIZE_MB} MB")
print(f"DRAM BW: {DRAM_BW_GBPS} GB/s | SSD BW: {SSD_BW_GBPS} GB/s")
print("-" * 65)
print(f"{'Cache Size':<12} | {'Hit Rate':<10} | {'Fetch Time (ms)':<16} | {'Speedup'}")
print("-" * 65)

cache_sizes = [4, 8, 16, 24, 32, 48, 60]

for size in cache_sizes:
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
                if len(cache) >= size:
                    cache.pop(0)
                cache.append(exp)
                
    hit_rate = hits / (hits + misses)
    
    # 1 MB = 1/1024 GB. Time (ms) = (GB / BW) * 1000
    data_hit_gb = (hits * EXPERT_SIZE_MB) / 1024.0
    data_miss_gb = (misses * EXPERT_SIZE_MB) / 1024.0
    
    time_dram_ms = (data_hit_gb / DRAM_BW_GBPS) * 1000.0
    time_ssd_ms = (data_miss_gb / SSD_BW_GBPS) * 1000.0
    total_time_ms = time_dram_ms + time_ssd_ms
    
    # Baseline: 0 cache (100% SSD misses)
    all_miss_gb = ((hits + misses) * EXPERT_SIZE_MB) / 1024.0
    baseline_time_ms = (all_miss_gb / SSD_BW_GBPS) * 1000.0
    
    speedup = baseline_time_ms / total_time_ms
    
    print(f"[{size:02d} experts] | {hit_rate*100:>6.2f}%   | {total_time_ms:>10.2f} ms       | {speedup:>5.2f}x")
