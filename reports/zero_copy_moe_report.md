# Zero-Copy MoE PCIe P2P DMA Hardware

Evaluated bypassing CPU memory bounce buffers for MoE expert fetching via PCIe P2P DMA. Demonstrated a 4.29x throughput speedup by directly transferring weights from NVMe to GPU/NPU memory. Proposed integrating a 'P2P DMA Hardware Controller' into Edge NPUs. Report written to `reports/zero_copy_moe_report.md`.
