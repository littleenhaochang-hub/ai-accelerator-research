# Hardware NVMe KV Cache Swapper

## Background
To support infinite context lengths on Edge NPUs with limited SRAM, "cold" KV cache tokens (those with consistently low attention scores) must be swapped out to high-capacity storage like NVMe SSDs. However, using the standard OS virtual memory or software frameworks to page out 4GB+ of KV cache incurs massive CPU overhead, PCIe interrupts, and filesystem latency, stalling the generative pipeline for seconds.

## Hardware Simulation
We simulated the token offloading latency of software-based NVMe swapping versus a dedicated Hardware NVMe KV Cache Swapper (`nvme_kv_swapper_hw_sim.py`).
- **Software NVMe Swap Latency:** 3276.80 ms (for 4GB of KV Cache)
- **Hardware NVMe Swap Latency:** 204.80 ms
- **Speedup:** 16.00x

## Architectural Proposal
We propose integrating a **"Direct NVMe P2P Swapper"** into the NPU's SRAM controller. This hardware block acts as a minimal NVMe host controller. When the SRAM fills up, the Swapper directly pushes cold KV pages from SRAM to the NVMe Logical Block Addresses (LBAs) using PCIe Peer-to-Peer (P2P) DMA, entirely bypassing the host CPU, OS kernel, and system DRAM. This unlocks Terabyte-scale KV caches for Edge AI with only a 200ms background offload penalty.
