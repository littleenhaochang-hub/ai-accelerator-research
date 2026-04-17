import numpy as np

def simulate_flatquant_outliers(dim=4096, tokens=1000, outlier_ratio=0.01):
    print("=== 4-bit FFN Outlier Flattening Simulation (FlatQuant) ===")
    
    # Generate activation distribution with extreme outliers
    activations = np.random.normal(0, 1, (tokens, dim))
    outlier_indices = np.random.choice(dim, int(dim * outlier_ratio), replace=False)
    activations[:, outlier_indices] *= 50.0 # Extreme outliers
    
    # Naive INT4 Quantization Error
    naive_scale = np.max(np.abs(activations)) / 7.0
    naive_quant = np.round(activations / naive_scale) * naive_scale
    naive_mse = np.mean((activations - naive_quant)**2)
    
    # Proposed: Channel-wise Affine Smoothing (FlatQuant)
    # Smooth out the outliers before quantization
    channel_max = np.max(np.abs(activations), axis=0)
    smoothing_factor = np.sqrt(channel_max) # Simplified smoothing
    smoothed_activations = activations / smoothing_factor
    
    flat_scale = np.max(np.abs(smoothed_activations)) / 7.0
    flat_quant = np.round(smoothed_activations / flat_scale) * flat_scale
    
    # Reconstruct
    reconstructed = flat_quant * smoothing_factor
    flat_mse = np.mean((activations - reconstructed)**2)
    
    sqnr_naive = 10 * np.log10(np.mean(activations**2) / naive_mse)
    sqnr_flat = 10 * np.log10(np.mean(activations**2) / flat_mse)
    
    print(f"Naive INT4 Quantization SQNR: {sqnr_naive:.2f} dB")
    print(f"FlatQuant INT4 Quantization SQNR: {sqnr_flat:.2f} dB")
    print(f"SQNR Improvement: {sqnr_flat - sqnr_naive:.2f} dB")

if __name__ == "__main__":
    simulate_flatquant_outliers()
