# Hardware Huffman MoE Decompressor

**Date:** 2026-04-29
**Context:** MoE Memory Bandwidth Optimization
**File:** `reports/huffman_moe_hw_report_zh.md`

## Summary
Evaluated Variable-Length Coding (Huffman) for compressing INT4 MoE expert weights down to an average of ~2.5 bits. Our simulation (`huffman_moe_hw_sim.py`) demonstrated a **2.31x fetch speedup**. 

## Hardware Implementation Proposal
Integrate an inline "Hardware Huffman Tree Decompressor" utilizing parallel SRAM look-up tables at the NPU Memory Controller. This allows weights to be stored in an ultra-compressed format in DRAM/UFS and decompressed on-the-fly during SRAM load with zero latency overhead.
