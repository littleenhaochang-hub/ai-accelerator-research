import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

print(f"Loading {model_id} (Warning: This is a massive model)...")
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="auto", 
    torch_dtype=torch.float16
)

# Generate a larger context to train the linear probe
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

early_layer = 2
target_layer = 16 # Mixtral has 32 layers, pick the middle
num_experts = 8
k = 2 # Mixtral routes to 2 experts

# Extract features (X) from Layer 2 and targets (Y) from target_layer
X = outputs.hidden_states[early_layer][0] # Shape: (seq_len, hidden_dim)
target_logits = outputs.router_logits[target_layer] # Shape: (seq_len, num_experts)

# Convert target logits to multi-hot vectors (1s for chosen experts, 0s elsewhere)
_, target_topk = torch.topk(target_logits, k=k, dim=-1)
Y = torch.zeros_like(target_logits)
Y.scatter_(1, target_topk, 1.0)

# Train/Test Split (80% train, 20% test)
seq_len = X.shape[0]
train_size = int(seq_len * 0.8)
test_size = seq_len - train_size

X_train, X_test = X[:train_size], X[train_size:]
Y_train, Y_test = Y[:train_size], Y[train_size:]
target_topk_test = target_topk[train_size:]

# Define a lightweight linear probe
probe = nn.Linear(X.shape[1], num_experts, dtype=X.dtype).to(model.device)
optimizer = torch.optim.AdamW(probe.parameters(), lr=0.01)
criterion = nn.BCEWithLogitsLoss()

print(f"\nTraining Linear Lookahead Predictor (Mixtral 8x7B)...")
print(f"Input: Layer {early_layer} Hidden States -> Output: Layer {target_layer} Experts")
print(f"Tokens: {train_size} train, {test_size} test")

epochs = 150
for epoch in range(epochs):
    optimizer.zero_grad()
    out = probe(X_train)
    loss = criterion(out, Y_train)
    loss.backward()
    optimizer.step()

# Evaluate the predictor on unseen test tokens
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
print(f"Model: Mixtral-8x7B-Instruct (8 Experts, Top-2 Routing)")
print(f"Lookahead Window: {target_layer - early_layer} layers")
print(f"Predictor Cache Hit Rate: {hit_rate*100:.2f}% (vs 25.0% random chance)")
print(f"Status: If hit rate > 75%, SSD latency can be effectively hidden.")