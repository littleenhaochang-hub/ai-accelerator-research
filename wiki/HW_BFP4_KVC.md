# HW-BFP4-KVC: Hardware Block-Floating-Point 4-bit KV Cache Engine

**Goal:** Radically compress KV cache for 64K+ context lengths on memory-constrained edge devices using FP4.
**Method:** Block-floating-point 4-bit quantization (block size 16) with a zero-cycle inline hardware dequantization engine.
**Results:** 3.56x latency speedup and 71.88% memory footprint reduction.

[Report](../reports/hw_bfp4_kvc_report_zh.md)
[Code](../hw_bfp4_kvc_sim.py)