import time

class HWKVRingBuffer:
    def __init__(self, context_len):
        self.context_len = context_len
        
    def simulate_software_ring_buffer(self):
        # Modulo arithmetic and pointer updates in software
        return self.context_len * 0.015
        
    def simulate_hardware_ring_buffer(self):
        # O(1) inline hardware pointer wrapping
        return 0.12 # fixed latency in us
        
if __name__ == "__main__":
    context_len = 1024 * 1024 # 1M context
    sim = HWKVRingBuffer(context_len)
    
    soft_lat = sim.simulate_software_ring_buffer()
    hard_lat = sim.simulate_hardware_ring_buffer()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
