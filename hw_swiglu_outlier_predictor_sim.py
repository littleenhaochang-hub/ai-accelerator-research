import random
import time

def simulate_swiglu_outliers(tokens, hw_prediction_enabled):
    print(f"Simulating SwiGLU Outliers for {tokens} tokens. HW Prediction: {hw_prediction_enabled}")
    
    # baseline 4-bit MAC array processing with outlier fallback
    total_time = 0
    total_energy = 0 # abstract units
    
    for _ in range(tokens):
        # 1% of activations are outliers that require FP16 MAC
        is_outlier = random.random() < 0.01
        
        if hw_prediction_enabled:
            # predictor costs 0.1 energy, perfectly routes to FP16 or INT4
            total_energy += 0.1
            if is_outlier:
                total_energy += 16.0 # FP16 MAC energy
                total_time += 0.002
            else:
                total_energy += 1.0 # INT4 MAC energy
                total_time += 0.001
        else:
            # without prediction, we must compute in FP16 or suffer accuracy loss,
            # or use a software sparsity pass which takes time
            # Assume software pass + selective FP16
            software_overhead = 0.005 # Software thresholding overhead per token
            total_time += software_overhead
            if is_outlier:
                total_energy += 16.0
                total_time += 0.002
            else:
                total_energy += 1.0
                total_time += 0.001
                
    return total_time, total_energy

baseline_time, baseline_energy = simulate_swiglu_outliers(10000, False)
hw_time, hw_energy = simulate_swiglu_outliers(10000, True)

print(f"Baseline Time: {baseline_time:.4f}s")
print(f"HW Predictor Time: {hw_time:.4f}s")
print(f"Speedup: {baseline_time/hw_time:.2f}x")
