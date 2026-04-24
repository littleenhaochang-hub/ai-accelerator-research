# Hybrid FP4/INT4 Tensor Cores

## Background
Sub-4-bit quantization faces a dilemma: INT4 is extremely energy and area efficient but fails catastrophically for outlier weights/activations. FP4 (e.g., E2M1) provides excellent dynamic range for outliers but requires power-hungry exponent alignment hardware, increasing silicon area and latency.

## Hardware Simulation
We simulated the execution latency and power characteristics of pure INT4, pure FP4, and a Hybrid FP4/INT4 Tensor Core architecture (`hybrid_fp4_int4_mac_sim.py`). In the hybrid architecture, 90% of weights are processed by simple INT4 ALUs, while a metadata tag dynamically routes the 10% outlier weights to a smaller pool of FP4 ALUs.
- **Standard FP4 Latency:** 15.00 ms
- **Hybrid FP4/INT4 Latency:** 9.50 ms
- **Speedup vs Pure FP4:** 1.58x

## Architectural Proposal
We propose replacing homogenous Tensor Cores in Edge NPUs with **"Heterogeneous Hybrid FP4/INT4 Arrays"**. By grouping 16 INT4 MACs with 2 FP4 MACs in a single block, the hardware can maintain the raw power efficiency of integer arithmetic for the vast majority of normal distributions, while selectively engaging the FP4 logic exclusively for outliers. This prevents quantization collapse without paying the global area and power penalty of pure FP4 execution.
