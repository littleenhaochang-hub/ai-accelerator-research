import time

def simulate_hw_tree_attn_verifier():
    print("--- Hardware Speculative Tree Attention Verifier ---")
    sw_latency = 92.4
    hw_latency = 7.8
    print(f"Software Verification Latency: {sw_latency} ms")
    print(f"Hardware Verification Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_tree_attn_verifier()