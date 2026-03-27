import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen1.5-MoE-A2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. This is why DRAM-less SSDs are cheaper but significantly slower for random I/O operations."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model(**inputs, output_router_logits=True, return_dict=True)

router_logits = outputs.router_logits
num_layers = len(router_logits)
seq_len = inputs.input_ids.shape[1]

# Extract top-4 experts for each layer
layer_experts = {}
for i in range(num_layers):
    probs = torch.nn.functional.softmax(router_logits[i], dim=-1)
    _, top_k = torch.topk(probs, k=4, dim=-1)
    layer_experts[i] = top_k

print(f"\n--- MoE Routing Predictability Analysis ---")
print(f"Total Layers: {num_layers} | Sequence Length: {seq_len} tokens")
print("Measuring how well early layers predict Layer 12's expert selection...\n")

target_layer = 12
target_indices = layer_experts[target_layer]

# How many of Layer 12's experts are already activated/predicted by Layer X?
for lookahead_layer in [11, 10, 8, 4, 2]:
    source_indices = layer_experts[lookahead_layer]
    
    total_requested = 0
    total_matched = 0
    
    for token_idx in range(seq_len):
        target_set = set(target_indices[token_idx].tolist())
        source_set = set(source_indices[token_idx].tolist())
        
        total_requested += len(target_set)
        # Intersection: how many experts needed in layer 12 were guessed in the early layer
        matches = len(target_set.intersection(source_set))
        total_matched += matches
        
    accuracy = total_matched / total_requested
    distance = target_layer - lookahead_layer
    print(f"Use Layer {lookahead_layer:02d} to predict Layer {target_layer} (Lookahead: {distance} layers) -> Match Rate: {accuracy*100:.2f}%")

print("\nConclusion: If match rate is high, we can issue async SSD prefetch requests during the early layer compute.")
