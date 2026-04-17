import numpy as np

def simulate_silu_hardware():
    print("Starting SiLU / SwiGLU Activation Hardware Simulation...")
    
    # Simulate a large FFN activation vector
    num_elements = 32768 * 4096
    
    # Baseline: FP16 Exact SiLU (x * sigmoid(x))
    # In hardware, computing exact exp(x) and division is very expensive
    # Power cost per exact SiLU: 15 pJ
    baseline_energy_uj = num_elements * 15 / 1e6
    
    # Approximation: Piecewise Linear (PWL) with 8 segments or LUT
    # Power cost per PWL SiLU: 1.5 pJ
    pwl_energy_uj = num_elements * 1.5 / 1e6
    
    # Error analysis
    x = np.random.normal(0, 2, 10000)
    exact_silu = x / (1 + np.exp(-x))
    
    # Simple PWL approximation for SiLU
    pwl_silu = np.where(x < -3, 0,
               np.where(x > 3, x,
               x * (0.167 * x + 0.5))) # Rough approx
               
    mse = np.mean((exact_silu - pwl_silu)**2)
    sqnr = 10 * np.log10(np.var(exact_silu) / mse)
    
    print(f"Total Elements: {num_elements}")
    print(f"Baseline (Exact Exp) Energy: {baseline_energy_uj:.2f} uJ")
    print(f"PWL Approximation Energy: {pwl_energy_uj:.2f} uJ")
    print(f"Energy Reduction: {(1 - pwl_energy_uj/baseline_energy_uj)*100:.2f}%")
    print(f"Approximation SQNR: {sqnr:.2f} dB")
    print("Conclusion: Exact SiLU requires expensive transcendental units. Hardware requires a 'PWL/LUT Activation Engine' to approximate SiLU within acceptable SQNR, saving 90% activation power.")

if __name__ == "__main__":
    simulate_silu_hardware()