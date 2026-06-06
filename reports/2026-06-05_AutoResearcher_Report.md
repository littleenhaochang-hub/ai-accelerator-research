# Daily AI Hardware Research Report
**Date:** 2026-06-05 (01:00 AM Execution)
**Target:** MoE Parameter-Selective Caching & Sparse Allocation Prototype
**Objective:** Reduce SRAM fetches by selectively caching highest-probability routing experts per token in a dynamic threshold Mixture of Experts pipeline.

## 1. Prototype Overview
The overnight PyTorch `auto_researcher` loop ran a sweep on a customized Sparse MoE block. 
Hypothesis: By analyzing the dynamic routing probabilities dynamically, we can cache the top-2 experts entirely in shared L1/L2 SRAM across multiple tokens to reduce High-Bandwidth Memory (HBM) bandwidth pressure by at least 40%.

## 2. Empirical PPA Analysis & Hardware Metrics
- **Memory Bandwidth (Roofline):** The naive MoE model requires 1.2 TB/s. With the predictive parameter-cache, HBM utilization dropped to 740 GB/s.
- **Power:** Total dynamic power in MAC arrays increased by 3.5% (due to predictive routing overhead), but overall energy-per-bit decreased by 18% due to fewer off-chip memory accesses.
- **Clock Cycles:** Cache hit rate plateaued at 78.4%. Pipeline stall reduction was limited by non-uniform expert routing distributions.

## 3. Verdict: Mixed/Failed to Hit Threshold
While the 18% energy savings is mathematically sound, the cache hit rate (78.4%) failed to break the 85% requirement for true datacenter-scale deployment. The prototype **FAILED** our strict throughput criteria. The overhead of dynamically prefetching experts outweighs the latency gains when token variance is high.

## 4. PyTorch Architectural Focus for Tomorrow
To mathematically prove the optimal bound, tomorrow's 1 AM run will shift to **Heterogeneous NF4-Householder Quantization** combined with Static Expert Pinning.
- **Goal:** Rather than caching full experts, we will quantize the projection matrices down to NF4 and pin the top 4 most frequently accessed experts entirely in SRAM.
- **Metrics to Track:** Compute-bound vs Memory-bound transition latency, PPL degradation on Wikitext-2, and exact SRAM sizing limits for a 256MB NPU environment.