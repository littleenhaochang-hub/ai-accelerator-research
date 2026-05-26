# HW-MLA-Absorber: Hardware MLA RoPE Absorber

**Goal:** Accelerate DeepSeek MLA operations by fusing Rotary Position Embeddings directly into up-projection.
**Method:** Inline hardware RoPE computation fused with MAC arrays to eliminate intermediate SRAM writes.
**Results:** 1.18x latency speedup vs separated execution.

[Report](../reports/hw_mla_absorber_report_zh.md)
[Code](../hw_mla_absorber_sim.py)