import time

def simulate_hw_spec_draft_verification():
    print("--- Hardware Speculative Draft Verification Accelerator ---")
    sw_latency = 88.0
    hw_latency = 6.0
    print(f"Software Verification Latency: {sw_latency} ms")
    print(f"Hardware Verification Latency: {hw_latency} ms")
    print(f"Speedup: {sw_latency/hw_latency:.2f}x")

if __name__ == '__main__':
    simulate_hw_spec_draft_verification()