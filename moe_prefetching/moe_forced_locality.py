import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen1.5-MoE-A2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. This is why DRAM-less SSDs are cheaper but significantly slower for random I/O operations."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model(**inputs, output_router_logits=True, return_dict=True)

# Target Layer 12
logits = outputs.router_logits[12]
if logits.dim() == 3:
    logits = logits[0]
seq_len, num_experts = logits.shape
k = 4
cache_size = 8

def simulate_cache(indices):
    cache = []
    hits = 0
    misses = 0
    unique = set()
    for i in range(len(indices)):
        req_experts = indices[i].tolist()
        unique.update(req_experts)
        for exp in req_experts:
            if exp in cache:
                hits += 1
                cache.remove(exp) # LRU update
                cache.append(exp)
            else:
                misses += 1
                if len(cache) >= cache_size:
                    cache.pop(0)
                cache.append(exp)
    return hits / (hits + misses), len(unique)

# 1. Baseline standard routing
probs_base = F.softmax(logits, dim=-1)
_, top_k_base = torch.topk(probs_base, k=k, dim=-1)
base_hit_rate, base_unique = simulate_cache(top_k_base)

# 2. Forced Locality (Temporal Smoothing)
# We apply a 1D convolution across the sequence length to smooth the logits.
# This forces adjacent tokens to "blend" their expert preferences, stabilizing routing.
window_size = 5
padding = window_size // 2

# Reshape for Conv1d: (batch=1, in_channels=num_experts, seq_len)
logits_t = logits.t().unsqueeze(0) 
kernel = torch.ones(num_experts, 1, window_size).to(logits.device) / window_size

smoothed_logits_t = F.conv1d(logits_t, kernel, padding=padding, groups=num_experts)
smoothed_logits = smoothed_logits_t.squeeze(0).t()

probs_smoothed = F.softmax(smoothed_logits, dim=-1)
_, top_k_smoothed = torch.topk(probs_smoothed, k=k, dim=-1)
smooth_hit_rate, smooth_unique = simulate_cache(top_k_smoothed)

print(f"--- Prototyping Forced Locality (Layer 12, {seq_len} tokens) ---")
print(f"Cache Size: {cache_size} experts")
print(f"\n[Baseline Routing]")
print(f"Unique Experts Activated: {base_unique} / {num_experts}")
print(f"Cache Hit Rate: {base_hit_rate*100:.2f}%")

print(f"\n[Forced Locality Routing (Window={window_size})]")
print(f"Unique Experts Activated: {smooth_unique} / {num_experts}")
print(f"Cache Hit Rate: {smooth_hit_rate*100:.2f}%")
print(f"\nImprovement: +{(smooth_hit_rate - base_hit_rate)*100:.2f}% hit rate")

# Performance Calculation
EXPERT_SIZE_MB = 32
DRAM_BW_GBPS = 95.0
SSD_BW_GBPS = 10.0

def calc_time(hit_rate, total_tokens, k):
    total_fetches = total_tokens * k
    hits = int(total_fetches * hit_rate)
    misses = total_fetches - hits
    
    data_hit_gb = (hits * EXPERT_SIZE_MB) / 1024.0
    data_miss_gb = (misses * EXPERT_SIZE_MB) / 1024.0
    
    time_dram_ms = (data_hit_gb / DRAM_BW_GBPS) * 1000.0
    time_ssd_ms = (data_miss_gb / SSD_BW_GBPS) * 1000.0
    
    return time_dram_ms + time_ssd_ms

base_time = calc_time(base_hit_rate, seq_len, k)
smooth_time = calc_time(smooth_hit_rate, seq_len, k)

print(f"\n--- Latency Evaluation (Layer 12) ---")
print(f"Assumed Expert Size: {EXPERT_SIZE_MB} MB | DRAM BW: {DRAM_BW_GBPS} GB/s | SSD BW: {SSD_BW_GBPS} GB/s")
print(f"Baseline Fetch Time:  {base_time:>8.2f} ms")
print(f"Smoothed Fetch Time:  {smooth_time:>8.2f} ms")
print(f"Speedup: {base_time / smooth_time:.2f}x")