import os
import psutil
import time
import math
import gc
from safetensors import safe_open
from huggingface_hub import snapshot_download
import glob

def get_memory_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

print("=== Pillar 3: Dynamic Expert Streaming Engine (Flash-to-RAM) ===")
MODEL_ID = "Qwen/Qwen1.5-MoE-A2.7B"

# Ensure we have the files
model_path = snapshot_download(MODEL_ID, allow_patterns=["*.safetensors"])
st_files = sorted(glob.glob(os.path.join(model_path, "*.safetensors")))

print("1. Indexing MoE Safetensors (Zero RAM Load)...")
tensor_index = {}
for st_file in st_files:
    with safe_open(st_file, framework="pt", device="cpu") as f:
        for k in f.keys():
            tensor_index[k] = st_file

print("\n2. Simulating Asynchronous Lookahead Expert Fetching...")
layer_idx = 1
# Qwen1.5-MoE-A2.7B has 60 experts, routes to 4.
predicted_experts = [2, 12, 19, 45]
print(f"   [Lookahead Predictor] Layer {layer_idx} experts needed: {predicted_experts} (Out of 60)")

# Build the exact list of tensor keys we need to extract from SSD
keys_to_load = []
prefix = f"model.layers.{layer_idx}."
total_layer_tensors = 0

for k in tensor_index.keys():
    if not k.startswith(prefix):
        continue
    total_layer_tensors += 1
    
    # 1. Attention logic
    if "self_attn" in k or "input_layernorm" in k or "post_attention_layernorm" in k:
        keys_to_load.append(k)
    # 2. Shared Expert & Router Gate
    elif "shared_expert" in k or "mlp.gate" in k:
        keys_to_load.append(k)
    # 3. Specific Experts (The magic happens here)
    elif "mlp.experts" in k:
        parts = k.split(".")
        exp_id = int(parts[5])
        if exp_id in predicted_experts:
            keys_to_load.append(k)

print(f"   Total tensors in Layer {layer_idx} (Dense Equivalent): {total_layer_tensors}")
print(f"   Tensors actually requested by Dynamic Streaming: {len(keys_to_load)}")

print("\n3. Executing DMA Transfer (Flash -> RAM) for Target Experts ONLY...")
gc.collect()
mem_before = get_memory_mb()
t0 = time.time()

loaded_tensors = {}
total_bytes_loaded = 0

# Group keys by file to optimize SSD reads
files_to_keys = {}
for k in keys_to_load:
    f = tensor_index[k]
    if f not in files_to_keys: files_to_keys[f] = []
    files_to_keys[f].append(k)

# The physical read from safetensors
for st_file, keys in files_to_keys.items():
    with safe_open(st_file, framework="pt", device="cpu") as f:
        for k in keys:
            tensor = f.get_tensor(k)
            loaded_tensors[k] = tensor
            total_bytes_loaded += tensor.numel() * tensor.element_size()

t1 = time.time()
mem_after = get_memory_mb()
payload_mb = total_bytes_loaded / (1024*1024)

print(f"   DMA Payload Size: {payload_mb:.2f} MB")
print(f"   RAM Footprint Increase: {mem_after - mem_before:.2f} MB")
print(f"   Flash Read Time: {(t1-t0)*1000:.2f} ms")

print("\n4. Comparative Analysis (What if we loaded the full layer?)")
full_layer_bytes = 0
for k, st_file in tensor_index.items():
    if k.startswith(prefix):
        with safe_open(st_file, framework="pt", device="cpu") as f:
            slice_view = f.get_slice(k)
            shape = slice_view.get_shape()
            numel = math.prod(shape)
            full_layer_bytes += numel * 2 # FP16

full_payload_mb = full_layer_bytes / (1024*1024)
print(f"   Full Layer Payload: {full_payload_mb:.2f} MB")

print(f"\n=== 🏆 Conclusion ===")
print(f"MoE Dynamic Streaming drastically cut the SSD read payload from {full_payload_mb:.1f} MB down to {payload_mb:.1f} MB.")
print(f"I/O Bandwidth & RAM Saved: {100 - (payload_mb/full_payload_mb)*100:.1f}%")
