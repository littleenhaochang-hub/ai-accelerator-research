# HW-STPM: Hardware Speculative Tree Pointer Manager

**Goal:** Accelerate Speculative Decoding (e.g., Medusa) by eliminating software overhead for drafting and rolling back token trees.
**Method:** Inline hardware memory management unit (MMU) tailored for tree-based KV pointer allocation and instant rollback.
**Results:** 50.00x latency speedup vs software tracking.

[Report](../reports/hw_spec_tree_pointers_report_zh.md)
[Code](../hw_spec_tree_pointers_sim.py)