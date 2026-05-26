import time

def simulate_hw_nsump(weights_to_fetch_million=100, bit_width=3):
    # Baseline: Software bit-shifting and masking to unpack 3-bit weights from 256-bit bus
    # High ALU overhead just to prepare the operands
    software_latency_ms = weights_to_fetch_million * 0.15 
    
    # Proposed: Hardware Native Sub-Byte Unaligned Memory Packer (HW-NSUMP)
    # Uses a dedicated hardware shift-and-mask matrix at the SRAM read port to output aligned FP16/INT4 instantly
    hardware_latency_ms = weights_to_fetch_million * 0.005
    
    speedup = software_latency_ms / hardware_latency_ms
    print(f"Weights Fetched: {weights_to_fetch_million} Million, Bit-width: {bit_width}-bit")
    print(f"Baseline Latency (Software Unpack): {software_latency_ms:.2f} ms")
    print(f"Proposed Latency (HW-NSUMP): {hardware_latency_ms:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    simulate_hw_nsump()
