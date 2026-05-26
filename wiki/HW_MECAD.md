# HW-MECAD: Hardware MoE Expert Caching and Asynchronous Decompression

**Goal:** Accelerate MoE decoding by eliminating CPU-GPU memory transfer bottlenecks.
**Method:** Asynchronous hardware decompressor and SRAM cache to hide fetch latency behind compute.
**Results:** 19.32x latency speedup vs PCIe baseline.

[Report](../reports/hw_mecad_moe_report_zh.md)
[Code](../hw_mecad_moe_sim.py)