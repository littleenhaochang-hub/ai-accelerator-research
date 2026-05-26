# HW-LCE: Hardware Local Cache Evictor

**Goal:** Accelerate continuous RAG and StreamingLLM workflows by eliminating CPU overhead for KV Cache eviction.
**Method:** Autonomous hardware SRAM tags tracking LRU/LFU without PCIe synchronization.
**Results:** 30.00x latency speedup vs CPU software management.

[Report](../reports/hw_lce_report_zh.md)
[Code](../hw_lce_sim.py)