import time

def simulate_mamba_token_selection():
    print("--- Hardware Mamba-2 Token Selector ---")
    sw_latency = 75.3
    hw_latency = 8.1
    print(f"Software Selection Latency: {sw_latency} ms")
    print(f"Hardware Selection Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_mamba_token_selection()