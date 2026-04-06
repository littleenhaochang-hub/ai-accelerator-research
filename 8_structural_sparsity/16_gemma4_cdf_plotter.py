import numpy as np
import matplotlib.pyplot as plt
import os

print("=== Gemma-4 26B MoE: CDF Plotter ===")

EXPERTS = 128
S = 1.2

ranks = np.arange(1, EXPERTS + 1)
probs = 1.0 / (ranks ** S)
probs /= np.sum(probs)
cdf = np.cumsum(probs) * 100

plt.figure(figsize=(10, 6))
plt.plot(ranks, cdf, marker='', linestyle='-', color='#d53f8c', linewidth=3)
plt.fill_between(ranks, cdf, color='#d53f8c', alpha=0.1)

# Annotations from the sweeping analysis
plt.axvline(x=20, color='#e53e3e', linestyle='--', alpha=0.8, label='20 Experts (3GB RAM) -> 77.3%')
plt.axvline(x=42, color='#3182ce', linestyle='--', alpha=0.8, label='42 Experts (5GB RAM) -> 87.3%')
plt.axvline(x=76, color='#38a169', linestyle='--', alpha=0.8, label='76 Experts (8GB RAM) -> 94.4%')

plt.title('Gemma-4 26B MoE: Expert CDF (Cumulative Hit Rate vs. Cached Experts)', fontsize=14)
plt.xlabel('Number of Experts Cached in DRAM (per Layer)', fontsize=12)
plt.ylabel('Cumulative Hit Rate (%)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(loc='lower right', fontsize=11)
plt.xlim(0, 128)
plt.ylim(0, 105)

plt.tight_layout()
os.makedirs('../reports', exist_ok=True)
plt.savefig('../reports/gemma4_expert_cdf.png', dpi=300)
print("CDF plot saved to ../reports/gemma4_expert_cdf.png")
