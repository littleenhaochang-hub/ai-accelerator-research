import torch
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def generate_long_tail_activation_heatmap():
    print("Simulating Gemma-4 26B FFN Activation Tensor (with long-tail outliers)...")
    
    # 模擬 4096 hidden dim 的 activation 分佈 (Batch=1, SeqLen=128, HiddenDim=4096)
    # 大部分數值在 -2 到 2 之間，但有極少數 outlier 高達 50-100
    np.random.seed(42)
    seq_len = 128
    hidden_dim = 4096
    
    # Base Gaussian distribution
    activations = np.random.normal(loc=0.0, scale=1.5, size=(seq_len, hidden_dim))
    
    # Inject long-tail outliers (0.1% of channels have massive outliers)
    num_outliers = int(hidden_dim * 0.001)
    outlier_channels = np.random.choice(hidden_dim, num_outliers, replace=False)
    
    for channel in outlier_channels:
        # Outliers can hit 50-100 magnitude
        activations[:, channel] = np.random.normal(loc=80.0, scale=20.0, size=seq_len)
        
    print(f"Generated Activations shape: {activations.shape}")
    print(f"Max Value: {np.max(activations):.2f}")
    print(f"99th Percentile: {np.percentile(activations, 99):.2f}")
    
    # 繪製熱圖 (為求視覺化清晰，只取部分 channels)
    viz_channels = 200
    viz_data = activations[:, :viz_channels]
    
    plt.figure(figsize=(14, 8))
    # 調整顏色範圍以凸顯 Outliers
    sns.heatmap(viz_data.T, cmap='viridis', vmax=10, vmin=-5, cbar_kws={'label': 'Activation Magnitude'})
    
    plt.title('Gemma-4 26B FFN Activation Heatmap (Simulated)\nHighlighting Long-Tail Outliers in Specific Channels', fontsize=16)
    plt.xlabel('Sequence Token Index', fontsize=12)
    plt.ylabel('Hidden Dimension Channel (Sampled)', fontsize=12)
    
    # Save the figure
    os.makedirs('../reports', exist_ok=True)
    out_path = '../reports/long_tail_activation_heatmap.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Heatmap saved to {out_path}")
    
if __name__ == "__main__":
    generate_long_tail_activation_heatmap()
