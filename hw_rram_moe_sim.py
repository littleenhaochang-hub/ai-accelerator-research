import math

def simulate_digital_router(num_tokens, num_experts, hidden_dim):
    # Digital MAC routing latency (Softmax + TopK)
    # O(N * E * D)
    latency_ms = (num_tokens * num_experts * hidden_dim) * 0.0000001
    power_mj = (num_tokens * num_experts * hidden_dim) * 0.00005
    return latency_ms, power_mj

def simulate_rram_router(num_tokens, num_experts, hidden_dim):
    # RRAM Crossbar Analog PIM Router
    # Constant time read out for analog MAC, massive power savings
    latency_ms = num_tokens * 0.0005 # dominated by ADC/DAC conversion
    power_mj = (num_tokens * num_experts * hidden_dim) * 0.0000002
    return latency_ms, power_mj

if __name__ == "__main__":
    tokens = 4096
    experts = 256
    dim = 4096
    
    dig_lat, dig_pwr = simulate_digital_router(tokens, experts, dim)
    rram_lat, rram_pwr = simulate_rram_router(tokens, experts, dim)
    
    speedup = dig_lat / rram_lat
    pwr_reduction = dig_pwr / rram_pwr
    
    print(f"Digital Router Latency: {dig_lat:.2f} ms")
    print(f"RRAM Router Latency: {rram_lat:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Power Reduction: {pwr_reduction:.2f}x")
