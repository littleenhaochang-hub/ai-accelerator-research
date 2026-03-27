import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "deepseek-ai/DeepSeek-Coder-V2-Lite-Base"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

print(f"Loading {model_id}...")
# Use bfloat16 to save memory (16B params = ~32GB RAM)
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="auto", 
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)

base_prompt = "Solid state drives (SSDs) use flash memory to store data persistently. Unlike traditional hard disk drives (HDDs) which use spinning magnetic platters, SSDs have no moving parts. This allows them to read and write data much faster. To manage the flash memory cells and communicate with the computer, SSDs use a controller. They also heavily rely on a DRAM cache. The DRAM cache stores the mapping tables that translate logical block addresses (used by the operating system) to physical page addresses (on the flash chips). When the CPU requests data, the SSD controller first checks the DRAM cache to find exactly where the data lives. If the mapping is in the DRAM cache, it's a 'cache hit' and the data can be retrieved immediately from the flash with minimal latency. If it's a 'cache miss', the controller has to read the mapping tables from the slower flash memory itself before it can even begin fetching the actual data, severely impacting performance. "
prompt = base_prompt * 5 
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("Running forward pass to extract hidden states and routing targets...")
with torch.no_grad():
    outputs = model(
        **inputs, 
        output_hidden_states=True, 
        output_router_logits=True, 
        return_dict=True
    )

# DeepSeek-V2-Lite has 27 layers. MoE starts at layer 1.
early_layer = 1
target_layer = 13
num_experts = 64 # DeepSeek-V2-Lite has 64 routed experts
k = 6 # DeepSeek-V2 routes to 6 experts (plus shared experts, but router_logits is for routed)

X = outputs.hidden_states[early_layer][0].float() # Cast to float for linear probe
# Note: DeepSeek models return router_logits as a tuple of tensors
# The first element is usually the router logits for the first MoE layer.
# We need to map target_layer to the index in router_logits.
# If MoE starts at layer 1, target_layer 13 corresponds to index 12 in router_logits.
router_idx = target_layer - 1 
target_logits = outputs.router_logits[router_idx].float()

_, target_topk = torch.topk(target_logits, k=k, dim=-1)
Y = torch.zeros_like(target_logits)
Y.scatter_(1, target_topk, 1.0)

seq_len = X.shape[0]
train_size = int(seq_len * 0.8)
test_size = seq_len - train_size

X_train, X_test = X[:train_size], X[train_size:]
Y_train, Y_test = Y[:train_size], Y[train_size:]
target_topk_test = target_topk[train_size:]

probe = nn.Linear(X.shape[1], num_experts).to(model.device)
optimizer = torch.optim.AdamW(probe.parameters(), lr=0.01)
criterion = nn.BCEWithLogitsLoss()

print(f"\nTraining Linear Lookahead Predictor ({model_id})...")
print(f"Input: Layer {early_layer} Hidden States -> Output: Layer {target_layer} Experts")
print(f"Tokens: {train_size} train, {test_size} test")

epochs = 150
for epoch in range(epochs):
    optimizer.zero_grad()
    out = probe(X_train)
    loss = criterion(out, Y_train)
    loss.backward()
    optimizer.step()

with torch.no_grad():
    test_out = probe(X_test)
    _, pred_topk = torch.topk(test_out, k=k, dim=-1)
    
    total_requested = 0
    total_matched = 0
    
    for i in range(len(target_topk_test)):
        target_set = set(target_topk_test[i].tolist())
        pred_set = set(pred_topk[i].tolist())
        total_requested += len(target_set)
        total_matched += len(target_set.intersection(pred_set))

hit_rate = total_matched / total_requested

print(f"\n--- Lookahead Prefetch Predictor Results ---")
print(f"Model: {model_id} ({num_experts} Experts, Top-{k} Routing)")
print(f"Lookahead Window: {target_layer - early_layer} layers")
print(f"Predictor Cache Hit Rate: {hit_rate*100:.2f}% (vs {k/num_experts*100:.2f}% random chance)")
