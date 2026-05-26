import time

class HWMCTSUCBEvaluator:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        
    def simulate_software_ucb(self):
        # Software iteration over nodes to calculate UCB (Upper Confidence Bound)
        # Involves math.sqrt, log, and memory fetches
        return self.num_nodes * 0.025
        
    def simulate_hardware_ucb(self):
        # O(1) parallel hardware comparator and ALU tree
        return 0.15 # fixed latency in us
        
if __name__ == "__main__":
    nodes = 4096
    sim = HWMCTSUCBEvaluator(nodes)
    
    soft_lat = sim.simulate_software_ucb()
    hard_lat = sim.simulate_hardware_ucb()
    
    speedup = soft_lat / hard_lat if hard_lat > 0 else 0
    
    print(f"Software Latency: {soft_lat:.2f} us")
    print(f"Hardware Latency: {hard_lat:.2f} us")
    print(f"Speedup: {speedup:.2f}x")
