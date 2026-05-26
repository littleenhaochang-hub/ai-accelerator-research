# HW-NUTQ: Hardware Non-Uniform Token Quantizer

**Goal:** Further compress KV Cache beyond INT4 by dynamically adjusting precision per token (from 1.58-bit to 8-bit).
**Method:** Inline hardware token importance predictor combined with variable-width memory allocation at the SRAM write port.
**Results:** 1.77x latency speedup and 43.40% memory reduction vs uniform INT4.

[Report](../reports/hw_nutq_report_zh.md)
[Code](../hw_nutq_sim.py)