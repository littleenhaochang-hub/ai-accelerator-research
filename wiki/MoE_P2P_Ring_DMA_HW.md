# MoE P2P Ring DMA Hardware

**Date:** 2026-04-28
**Context:** MoE Memory Transfer Optimization
**File:** `reports/moe_p2p_ring_dma_report_zh.md`

## Summary
To solve the CPU-GPU memory transfer bottleneck during MoE decoding, we proposed and simulated an Asynchronous PCIe P2P Ring DMA architecture. 
By allowing direct NVMe-to-NPU (or GPU) DMA transfers and bypassing the CPU bounce buffers, our simulation (`moe_p2p_ring_dma_sim.py`) demonstrated a latency reduction from 203.49ms down to 44.45ms, achieving a **4.58x speedup**.

## Hardware Implementation Proposal
Integrate a dedicated "P2P Ring DMA Hardware Controller" directly into the Edge NPU to handle expert fetches autonomously based on routing logic, keeping the primary MAC arrays fed without CPU/OS intervention.
