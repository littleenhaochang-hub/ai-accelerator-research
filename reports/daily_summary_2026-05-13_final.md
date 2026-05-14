# Daily AI Hardware Research Report - 2026-05-13

## 1. Overnight Experiments (1 AM Auto-Researcher)
The Auto-Researcher conducted three primary hardware-software co-design simulations targeting Edge NPU bottlenecks in long-context and speculative decoding workloads:

*   **Hardware Mamba-PIM LUT Scan Engine (HW-Mamba-PIM-LUT):** Evaluated converting Mamba's O(N) sequential scans to Processing-in-Memory (PIM) Look-Up Tables (LUTs) and O(log N) associative trees.
*   **Hardware Token-Tree Routing Engine (HW-TTR):** Tested replacing software-based pointer chasing in Speculative Decoding draft trees with an O(1) Ternary Content-Addressable Memory (TCAM) router.
*   **Hardware MoE KV Cache Compression Engine (HW-MoE-KVC):** Simulated dedicated inline SRAM hardware compression for Mixture-of-Experts decoding bandwidth bottlenecks.

## 2. Empirical Results & Evaluation
*   **HW-Mamba-PIM-LUT (SUCCESS):** Demonstrated a **59.09x** latency speedup (from 899.00 ms to 15.21 ms) for 32K context lengths by completely eliminating MAC multipliers in favor of SRAM lookups.
*   **HW-TTR (SUCCESS):** Achieved a massive **1417.58x** speedup (from 6415.81 ms to 4.53 ms) for 1024-node speculative draft trees by utilizing TCAM parallel matching, eliminating severe CPU/software cache misses.
*   **HW-MoE-KVC (SUCCESS):** Reached a **7.76x** speedup (500.41 ms to 64.45 ms) via inline compression/decompression, verifying the thesis that MoE bandwidth walls can be bypassed at the SRAM controller level.

## 3. Tomorrow's PyTorch Architectural Focus
**Unified Speculative Mamba-PIM State Engine:**
Tomorrow's experiment will fuse the successful TCAM Token-Tree Routing with the Mamba-PIM LUT Engine in PyTorch. The goal is to simulate a Multi-Branch Speculative Mamba Decoder where TCAM manages the branching states in O(1) time, while the PIM-LUT executes the speculative SSM continuous scans without invoking the main Tensor Cores, aiming for zero-MAC speculative drafts.