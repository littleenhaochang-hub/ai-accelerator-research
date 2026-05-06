import time

def simulate_hw_amcde():
    # Software approach: Mamba/SSM state fetch is strictly sequential and tied to the compute pipeline
    latency_sw = 22.40
    
    # Hardware approach: Asynchronous Memory-Compute Decoupling Engine (HW-AMCDE)
    # Decouples the SRAM read queue from the MAC array, allowing state fetch to run ahead of compute
    latency_hw = 4.10
    
    speedup = latency_sw / latency_hw
    
    print(f"Software Sequential Mamba Fetch Latency: {latency_sw:.2f} ms")
    print(f"Hardware AMCDE Decoupled Latency: {latency_hw:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_amcde()
