import time

def standard_layer_execution(tokens, layers):
    # Standard layer-by-layer execution. Wait for all tokens to finish layer L before L+1
    # Introduces pipeline bubbles for token generation
    latency = tokens * layers * 0.01 
    bubble_overhead = tokens * 0.005
    return latency + bubble_overhead

def micro_pipeline_hw_execution(tokens, layers):
    # Hardware Micro-Pipeline Parallelism
    # Token T goes to layer L+1 the exact clock cycle it finishes layer L.
    # No waiting for T+1. Zero pipeline bubbles.
    latency = (tokens * 0.01) + (layers * 0.01) # Overlapped execution
    return latency

def main():
    tokens = 1000
    layers = 32
    
    print("Running Hardware Micro-Pipeline Parallelism Simulation...")
    std_lat = standard_layer_execution(tokens, layers)
    print(f"Standard Layer-by-Layer Latency: {std_lat:.2f} ms")
    
    hw_lat = micro_pipeline_hw_execution(tokens, layers)
    print(f"Hardware Micro-Pipeline Latency: {hw_lat:.2f} ms")
    
    speedup = std_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
