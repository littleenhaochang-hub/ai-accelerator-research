# HW-TTCR: Hardware Test-Time Compute Router

**Goal:** Accelerate System 2 thinking models (like o1/DeepSeek-R1) on edge devices by eliminating CPU synchronization during Test-Time Compute scaling.
**Method:** Inline hardware evaluator to check confidence scores and dynamically route tokens to output or MCTS expansion.
**Results:** 250.00x latency speedup vs software routing.

[Report](../reports/hw_ttcr_report_zh.md)
[Code](../hw_ttcr_sim.py)