import time

class HWSparseExpertPredictor:
    def __init__(self, experts, tokens):
        self.experts = experts
        self.tokens = tokens
        
    def simulate_software_routing(self):
        # Software softmax + top-k
        return self.experts * self.tokens * 0.005
        
    def simulate_hardware_predictor(self):
        # O(1) sparse predictor
        return 10.5 # fixed latency in us
        
if __name__ == "__main__":
    experts = 256
    tokens = 4096
    sim = HWSparseExpertPredictor(experts, tokens)
    
    soft_lat = sim.simulate_software_routing()
    hard_lat = sim.simulate_hardware_predictor()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
