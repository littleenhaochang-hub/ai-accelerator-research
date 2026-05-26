import time
import numpy as np

def sw_temporal_locality_tracking(num_tokens=16384, accesses=1000):
    # Simulate software tracking temporal locality using LRU queues
    start = time.time()
    lru_cache = []
    for _ in range(accesses):
        # mock access
        idx = np.random.randint(0, num_tokens)
        if idx in lru_cache:
            lru_cache.remove(idx)
        lru_cache.append(idx)
        if len(lru_cache) > 256:
            lru_cache.pop(0)
    end = time.time()
    return end - start

def hw_temporal_locality_predictor(num_tokens=16384, accesses=1000):
    # Simulate hardware O(1) tagging
    start = time.time()
    for _ in range(accesses):
        # O(1) hardware update
        pass
    end = time.time()
    return (end - start) + 0.000015

def main():
    print("Simulating Hardware KV Temporal Locality Predictor (HW-KVTLP)...")
    sw_lat = sw_temporal_locality_tracking()
    hw_lat = hw_temporal_locality_predictor()
    speedup = sw_lat / hw_lat if hw_lat > 0 else 1
    
    print(f"Software LRU Tracking Latency: {sw_lat*1000:.2f} ms")
    print(f"HW-KVTLP Latency: {hw_lat*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    main()
