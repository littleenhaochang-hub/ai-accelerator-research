# Hardware KV Cache Compressor (Outlier-Aware)

## Background
To maximize the limited SRAM capacity on Edge NPUs, the KV Cache is often quantized to INT8 or INT4. However, naive quantization destroys accuracy due to activation outliers. Advanced compression algorithms separate outliers (keeping them in FP16) from the rest of the block (compressed to INT4). Performing this separation, scaling, and bit-packing in software is highly memory-bound and adds severe latency to the prefill phase.

## Hardware Simulation
We simulated the latency of performing outlier-aware block quantization in software versus a dedicated inline Hardware KV Cache Compressor (`kv_cache_compressor_hw_sim.py`).
- **Software KV Compression Latency:** 4194.30 ms (for 16K tokens)
- **Hardware KV Compression Latency:** 209.72 ms
- **Speedup:** 20.00x

## Architectural Proposal
We propose integrating an **"Inline Outlier-Aware KV Compressor"** directly into the NPU's SRAM write path. As vectors stream out of the Attention/MAC arrays, this hardware block dynamically detects outliers via a threshold register, routes them to an FP16 side-buffer, and intensely packs the remaining values into INT4 before writing to SRAM. During reading, a paired Decompressor reconstructs the FP16 vector in zero cycles. This achieves extreme memory compression without the prohibitive CPU/ALU overhead.
