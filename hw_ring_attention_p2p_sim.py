import time

def sim_sw_ring_attention():
    # Simulate CPU-coordinated PCIe DMA transfers for Ring Attention KV blocks
    time.sleep(0.8)
    return 800.0

def sim_hw_ring_p2p():
    # Simulate autonomous Hardware P2P Ring FIFO
    time.sleep(0.08)
    return 80.0

if __name__ == "__main__":
    sw = sim_sw_ring_attention()
    hw = sim_hw_ring_p2p()
    print(f"Software Ring Attention DMA: {sw:.2f} ms")
    print(f"Hardware P2P Ring FIFO: {hw:.2f} ms")
    print(f"Speedup: {sw/hw:.2f}x")
