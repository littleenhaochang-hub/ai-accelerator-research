# HW-SKCP: Hardware Sparse K-Cache Predictor

**Goal:** Reduce memory bandwidth bottlenecks during generation for extremely long context (128K+).
**Method:** Inline hardware predictor to fetch only high-attention K-Cache blocks from DRAM.
**Results:** 10.00x latency speedup vs dense baseline.

[Report](../reports/hw_skcp_report_zh.md)
[Code](../hw_skcp_sim.py)