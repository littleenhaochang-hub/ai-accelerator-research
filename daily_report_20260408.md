# Daily AI Hardware Research Report - April 8, 2026

## 1. Overnight Experiment Summary (1:00 AM)
**Target:** Decoupling Expert Fetch for Memory-Bound Test-Time Compute (TTC)
**Artifact Generated:** `ttc_moe_prefetch_baseline.py`

The Auto-Researcher initiated a run investigating the combination of Test-Time Compute (TTC) branching with lookahead MoE (Mixture of Experts) prefetching. The primary architectural goal was to decouple the expert weight fetch phase from the main compute pipeline. By predicting expert usage via the router earlier in the pipeline execution (lookahead), the prototype attempted to hide the massive memory latency inherently tied to high-parameter MoE switching.

## 2. Empirical Evaluation & Result Analysis
**Outcome: FAILED (Wall-Clock PPA)**

**Architectural Analysis (Roofline & PPA):**
While the simulated forward pass completed successfully, the prototype failed to achieve any genuine wall-clock acceleration. 
- **The Bottleneck:** The implementation relied on standard synchronous PyTorch semantics. The `_dispatch_prefetch_signal` is logically sound but physically ineffective without an underlying asynchronous DMA mechanism.
- **Memory Wall Reality:** Fetching weights dynamically across the memory hierarchy (HBM -> SRAM) sequentially blocks the SMs (Streaming Multiprocessors). We cannot overcome the Memory Wall simply by changing the mathematical execution graph; the physical data flow stalled due to a lack of overlapping I/O and compute.

**Conclusion:** The mathematical routing logic was validated, but from a silicon/hardware co-design perspective, the prototype failed due to memory bandwidth saturation and synchronous dispatch constraints. 

## 3. Tomorrow's Architectural Focus (PyTorch)
To salvage the lookahead routing concept, tomorrow's iteration must abandon synchronous module execution. The focus will shift to:
1. **Asynchronous DMA Overlap:** Implementing custom Triton/CUDA kernels to enforce strict overlap between MAC execution (current layer) and HBM-to-SRAM DMA prefetching (next layer experts).
2. **Spatial SRAM Partitioning:** Modifying the PyTorch layout to pin the highest-probability expert branches statically in SRAM, only dynamically fetching the tail distribution.
3. **Target Script:** Develop `async_ttc_dma_pipeline.py` with explicit `torch.cuda.current_stream()` management.

*Every picojoule matters. Every clock cycle counts.*
