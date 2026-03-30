# Prototyping Google's TurboQuant (ICLR 2026)

This folder contains a PyTorch simulation of the **TurboQuant** algorithm, introduced by Google (accepted to ICLR 2026). The algorithm targets the massive memory bottleneck caused by the Key-Value (KV) Cache in Large Language Models (LLMs) during long-context inference.

## The Problem
Standard LLM inference stores the KV cache in FP16 (16 bits per value). A 100,000-token context for a 3B/4B parameter model requires approximately ~3.7 GB of Unified Memory/VRAM just for the cache. This causes Edge devices (like Apple Silicon Macs) to easily run Out-Of-Memory (OOM) on long inputs.

## The TurboQuant Solution
TurboQuant compresses the KV cache to ~3-4 bits per value with near-zero accuracy loss. It achieves this via a two-stage process:

1. **PolarQuant (Random Rotation):** Instead of standard linear quantization (which struggles with outlier values in LLM activations), TurboQuant applies a random orthogonal rotation matrix to the vectors. This evenly distributes the outliers across all dimensions, allowing extreme compression (down to 3 bits) without catastrophic information loss.
2. **QJL (Quantized Johnson-Lindenstrauss) Residuals:** To fix the errors introduced by the 3-bit compression, TurboQuant calculates the residual error and stores *only its sign* (1 bit). During the attention dot-product, this 1-bit residual acts as an unbiased estimator to correct the math.

## Prototype Results
Running `turboquant_prototype.py` simulates this process on a 4,096 sequence length KV Cache block:
* **Original Size (FP16):** 8.00 MB
* **TurboQuant Size (4-bit):** 2.00 MB (4x Reduction)
* **Reconstruction Accuracy (Cosine Similarity):** ~90.5%

By reducing the memory footprint by 4x to 6x, TurboQuant enables Edge AI accelerators to run 200K+ token contexts entirely in SRAM/Unified Memory without fetching from the SSD.
