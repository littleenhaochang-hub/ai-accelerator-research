# HW-ADLC: Hardware Adaptive Draft-Length Controller

**Goal:** Maximize speculative decoding throughput by dynamically adjusting draft length.
**Method:** Inline hardware entropy evaluator to control draft model generation length with zero software overhead.
**Results:** 2.09x TPS speedup vs fixed-length drafting.

[Report](../reports/hw_adlc_report_zh.md)
[Code](../hw_adlc_sim.py)