import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer
model_id = "Qwen/Qwen1.5-MoE-A2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

# Prepare input prompt
prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. This is why DRAM-less SSDs are cheaper but significantly slower for random I/O operations."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Get router logits to simulate expert selection
with torch.no_grad():
    outputs = model(**inputs, output_router_logits=True, return_dict=True)

# Focus on router logits from a specific layer (e.g., layer 12)
logits = outputs.router_logits[12] 
probs = torch.nn.functional.softmax(logits, dim=-1)
_, top_k_indices = torch.topk(probs, k=4, dim=-1) # Assuming top-k routing

# --- Hardware Assumptions (Baseline for BF16/FP16 weights) ---
BASE_EXPERT_SIZE_MB = 32 # Approx size of one expert in this model (e.g., assuming BF16/FP16 precision)
DRAM_BW_GBPS = 95.0
SSD_BW_GBPS = 10.0

# --- Hardware-Accelerated Mixed-Precision Quantization Parameters ---
# Experts are stored at this low bit-width
QUANT_BIT_WIDTH = 4 # e.g., INT4 for storage/cache on SSD and DRAM
# Original precision for which BASE_EXPERT_SIZE_MB is estimated
BASE_PRECISION_BIT_WIDTH = 16 # e.g., BF16
# Target precision after on-chip dequantization for compute units
DEQUANT_PRECISION_BIT_WIDTH = 16 # e.g., BF16 or INT8

# On-chip dequantization latency per expert. This represents the fixed overhead
# for the dequantization engine to convert weights to higher precision.
# Ideally pipelined, but for simulation, we account for a small, non-zero overhead.
DEQUANT_LATENCY_PER_EXPERT_MS = 0.005 # e.g., 5 microseconds

# Calculate the effective expert size in storage/cache due to quantization
# This directly impacts data transfer volume.
quant_reduction_factor = BASE_PRECISION_BIT_WIDTH / QUANT_BIT_WIDTH
EFFECTIVE_EXPERT_SIZE_MB = BASE_EXPERT_SIZE_MB / quant_reduction_factor

print(f"\n--- MoE Prefetch Performance Simulation (Layer 12) ---")
print(f"Sequence Length: {inputs.input_ids.shape[1]} tokens")
print(f"Assumed Baseline Expert Size (e.g., BF{BASE_PRECISION_BIT_WIDTH}): {BASE_EXPERT_SIZE_MB} MB")
print(f"DRAM BW: {DRAM_BW_GBPS} GB/s | SSD BW: {SSD_BW_GBPS} GB/s")
print("-" * 65)

print(f"\n--- Proposed Hardware-Accelerated Mixed-Precision Expert Quantization Scheme ---")
print(f"Storage/Cache Precision: INT{QUANT_BIT_WIDTH} (from BF{BASE_PRECISION_BIT_WIDTH})")
print(f"Effective Expert Size in Storage/Cache: {EFFECTIVE_EXPERT_SIZE_MB:.2f} MB ({quant_reduction_factor:.0f}x reduction)")
print(f"On-chip Dequantization Latency per Expert: {DEQUANT_LATENCY_PER_EXPERT_MS*1000:.0f} µs (to BF{DEQUANT_PRECISION_BIT_WIDTH} for compute)")
print("-" * 65)
print(f"{'Cache Size':<12} | {'Hit Rate':<10} | {'Fetch + Dequant Time (ms)':<25} | {'Speedup vs. Baseline'}")
print("-" * 65)

# Simulate different DRAM cache sizes
cache_sizes = [4, 8, 16, 24, 32, 48, 60]

for size in cache_sizes:
    cache = [] # Represents the experts currently in DRAM cache (LRU)
    hits = 0
    misses = 0
    
    # Simulate expert access pattern
    for i in range(len(top_k_indices)): # For each token's selected experts
        req_experts = top_k_indices[i].tolist() # List of expert IDs requested
        for exp in req_experts:
            if exp in cache:
                hits += 1
                cache.remove(exp) # Move to front (LRU policy)
                cache.append(exp)
            else:
                misses += 1
                if len(cache) >= size: # Cache is full, evict LRU
                    cache.pop(0)
                cache.append(exp) # Add new expert to cache
                
    hit_rate = hits / (hits + misses)
    total_expert_accesses = hits + misses
    
    # Calculate data transfer volumes using the EFFECTIVE_EXPERT_SIZE_MB
    # 1 MB = 1/1024 GB. Time (ms) = (GB / BW_GBPS) * 1000
    data_hit_gb = (hits * EFFECTIVE_EXPERT_SIZE_MB) / 1024.0
    data_miss_gb = (misses * EFFECTIVE_EXPERT_SIZE_MB) / 1024.0
    
    time_dram_ms = (data_hit_gb / DRAM_BW_GBPS) * 1000.0
    time_ssd_ms = (data_miss_gb / SSD_BW_GBPS) * 1000.0
    
    # Add dequantization latency for ALL experts fetched (whether from DRAM or SSD)
    dequant_time_ms = total_expert_accesses * DEQUANT_LATENCY_PER_EXPERT_MS
    
    # Total time for the proposed scheme
    total_time_ms = time_dram_ms + time_ssd_ms + dequant_time_ms
    
    # --- Baseline for speedup comparison ---
    # The baseline assumes no quantization, so it uses BASE_EXPERT_SIZE_MB.
    # It also assumes a pessimistic scenario where ALL experts must be fetched from SSD.
    baseline_all_miss_gb = (total_expert_accesses * BASE_EXPERT_SIZE_MB) / 1024.0
    baseline_time_ms = (baseline_all_miss_gb / SSD_BW_GBPS) * 1000.0
    
    speedup = baseline_time_ms / total_time_ms
    
    print(f"[{size:02d} experts] | {hit_rate*100:>6.2f}%   | {total_time_ms:>21.2f} ms | {speedup:>20.2f}x")