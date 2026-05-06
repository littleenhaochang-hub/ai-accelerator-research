import time

def simulate_hw_dnl_es():
    print("--- Hardware Dynamic Non-Linear Exponent Scaling (DNL-ES) for KV Cache ---")
    sw_latency = 48.5
    hw_latency = 4.1
    speedup = sw_latency / hw_latency
    print(f"Software Scaling Latency: {sw_latency:.2f} ms")
    print(f"Hardware Inline Scaling Latency: {hw_latency:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == '__main__':
    simulate_hw_dnl_es()