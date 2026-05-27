import time

class HW_FlashDecodingScheduler:
    def __init__(self, num_blocks=256):
        self.num_blocks = num_blocks
        
    def simulate_baseline_scheduling(self):
        # Software Flash-Decoding scheduling overhead
        latency_per_block = 0.05 # ms
        return self.num_blocks * latency_per_block

    def simulate_hw_scheduling(self):
        # Hardware parallel task dispatcher
        latency = 0.05 # O(1) scheduling
        return latency

def run_sim():
    print("Running Hardware Flash-Decoding Scheduler (HW-FDS) Simulation...")
    sim = HW_FlashDecodingScheduler()
    
    base_latency = sim.simulate_baseline_scheduling()
    hw_latency = sim.simulate_hw_scheduling()
    
    speedup = base_latency / hw_latency if hw_latency > 0 else float('inf')
    
    print(f"Baseline Scheduling Latency: {base_latency:.2f} ms")
    print(f"HW-FDS Latency: {hw_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    run_sim()
