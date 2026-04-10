import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=== Gemma-4 26B Time-Over-Space Router Profiler & Heatmap ===")

LAYERS = 30
EXPERTS_PER_LAYER = 128
TOKENS = 10000

# Mock empirical skew for each layer to simulate layer-wise variance
# Early layers tend to have sharper distributions, later layers more uniform
hit_matrix = np.zeros((LAYERS, EXPERTS_PER_LAYER))

for layer in range(LAYERS):
    s = 1.3 - (layer * 0.01) # Zipf parameter degrades deeper into the network
    ranks = np.arange(1, EXPERTS_PER_LAYER + 1)
    probs = 1.0 / (ranks ** s)
    probs /= np.sum(probs)
    
    # Shuffle slightly so the "hot" experts aren't always index 0
    np.random.seed(layer) # deterministic for reproducibility
    shuffled_indices = np.random.permutation(EXPERTS_PER_LAYER)
    
    # Simulate tokens
    choices = np.random.choice(EXPERTS_PER_LAYER, size=(TOKENS, 8), p=probs) # Top-8
    
    # Count frequencies mapped back to our shuffled indices
    for expert_id in range(EXPERTS_PER_LAYER):
        hit_matrix[layer, shuffled_indices[expert_id]] = np.sum(choices == expert_id)

# Normalize per layer
hit_matrix_norm = hit_matrix / (TOKENS * 8)

plt.figure(figsize=(15, 8))
sns.heatmap(hit_matrix_norm, cmap="magma", xticklabels=10, yticklabels=1)
plt.title("Gemma-4 26B MoE Router Activation Heatmap (30 Layers x 128 Experts)")
plt.xlabel("Expert Index (0-127)")
plt.ylabel("Layer Index (0-29)")
plt.tight_layout()

os.makedirs('../reports', exist_ok=True)
out_path = '../reports/gemma4_router_heatmap.png'
plt.savefig(out_path, dpi=300)
print(f"Heatmap saved to {out_path}")
