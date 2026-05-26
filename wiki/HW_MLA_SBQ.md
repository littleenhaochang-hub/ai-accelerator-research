# HW-MLA-SBQ: Hardware MLA Sub-Byte Quantizer

**Goal:** Accelerate DeepSeek MLA latent vector fetching for 128K+ long context models on edge devices.
**Method:** Compress MLA latent vectors to 2-bit with an inline hardware decompressor at the SRAM read port.
**Results:** 7.99x latency speedup vs FP16 baseline.

[Report](../reports/hw_mla_sbq_report_zh.md)
[Code](../hw_mla_sbq_sim.py)