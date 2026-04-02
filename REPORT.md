# AI Accelerator Research Report
**Target Bottleneck:** Test-Time Compute (TTC) Branching and Warp Divergence
**Date:** 2026-03-31

## Executive Summary
Recent papers from ISCA and HPCA 2026 highlight a significant hardware bottleneck in large-batch LLM inference and reasoning models (like o1/o3): **dynamic branching and warp divergence** during test-time compute scaling. As models allocate variable compute budgets to different tokens, the GPU's SIMT execution model suffers from severe underutilization and uncoalesced memory accesses when executing divergent expert paths.

## Proposed Baseline Architecture
We developed a PyTorch prototype `baseline_ttc_branching.py` that implements a Test-Time Compute Routing Network. This architecture dynamicly scales the number of activated branches based on a `test_time_budget` scalar. To mitigate the warp divergence bottleneck observed in naive implementations, we propose:

1.  **Hardware-Aware Token Sorting:** Grouping tokens with the same active branches before dispatching to expert kernels to maximize warp utilization.
2.  **Lookup Table (LUT) Assisted Routing:** Using low-precision SRAM LUTs to quickly estimate routing probabilities and prefetch expert weights into L2 cache, preventing DRAM bandwidth saturation during dynamic compute scaling.

## Auto-Researcher Optimizations Across 7 Pillars
The `auto_researcher.py` script iteratively validated the architecture against:
- **Test-Time Compute branching:** Implemented hardware token sorting.
- **RetNet/Mamba parallel scans:** Ensured sequential routing states are parallelizable using prefix-sum.
- **W4A4 QJL quantization:** Applied 4-bit weight quantization to expert branches to maximize L2 capacity.
- **MoE prefetching:** Scheduled asynchronous memory fetches for experts during the routing phase.
- **KV Cache compression:** Paged TTC states into compressed CPU memory for extreme long-context generation.
- **PIM activations:** Explored AQPIM-style in-memory quantization for the routing logits.
- **CXL CPU-GPU hybrid offloading:** Verified hybrid offloading for low-probability expert branches to Intel AMX accelerators.

## Next Steps
RTL design (SystemVerilog) for the token sorting and prefetching logic.
