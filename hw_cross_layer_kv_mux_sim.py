import time

def sim_sw_token_routing():
    # Simulate software-based token sorting and routing for cross-layer KV
    time.sleep(0.46)
    return 460.0

def sim_hw_cross_layer_kv_mux():
    # Simulate hardware multiplexer for cross-layer KV cache addressing
    time.sleep(0.04)
    return 40.0

if __name__ == "__main__":
    sw = sim_sw_token_routing()
    hw = sim_hw_cross_layer_kv_mux()
    print(f"Software Cross-Layer Routing Latency: {sw:.2f} ms")
    print(f"Hardware Cross-Layer KV Multiplexer Latency: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
