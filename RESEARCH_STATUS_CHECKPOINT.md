# AI Accelerator Research - Status Checkpoint
**Date:** March 30, 2026

This document serves as the master state-tracker for the AI Accelerator Research repository. It summarizes all experimental findings, architectural decisions, and current prototype statuses across the active research pillars.

---

## Pillar 1: Model Architecture

### 1.2 SSM / Mamba Hybrids (`1_2_ssm_mamba_hybrids`)
- **Status:** PyTorch Prototypes Completed.
- **Findings:** At 4K context, standard $O(N^2)$ GEMM attention outpaces naive $O(N)$ sequential RNN scans on Apple Silicon (MPS). 
- **Solution:** Developed `block_parallel_scan.py` to simulate a hardware-aware chunked parallel scan. It successfully breaks the $O(N)$ sequential dependency, mimicking $O(\log N)$ Triton/Metal thread-block execution.
- **Next Steps:** Lowering the block-parallel logic into actual Apple Metal shaders.

### 1.3 Linear Sliding Window (`1_3_linear_sliding_window`)
- **Status:** Prototyped and Exported.
- **Findings:** Implemented an $O(N)$ sliding window attention block tailored for 32K DOM parsing contexts. It efficiently bypasses the massive memory blowup of full $O(N^2)$ attention.
- **Deployment:** Successfully traced and compiled the PyTorch graph into a pure `sliding_window.tflite` model using the Google `litert-torch` toolchain. Ready for edge deployment profiling.

---

## Pillar 4: Memory-Centric (KV Cache & Attention)

### 4.3 TurboQuant & A4 Fusion (`4_3_kv_cache_turboquant`)
- **Status:** Evaluated and Resolved the "Softmax Cliff".
- **Findings:** Fusing 4-bit activations (A4) with 4-bit rotated KV Cache (TurboQuant) causes quantization variance to compound ($e_q \cdot e_k$). The Softmax function exponentially amplifies this noise, destroying the Signal-to-Noise Ratio (SNR) and causing a 0% pass rate in live text generation.
- **The Fix (1-Bit QJL):** We implemented a 1-bit residual correction (+1/-1 sign of the compression error). Adding this to the hardware MAC via Popcount recovers +4.18 dB of SNR.
- **Live Validation:** Monkey-patched a live `Qwen2.5-0.5B-Instruct` model. While standard A4A4 collapsed into silence or gibberish, the 5-bit QJL pipeline successfully recovered semantic English generation (40-60% task pass rate).

---

## Pillar 2: Quantization

### 2.3 Classical A4A4 Optimizations (`2_3_a4a4_attention_optimizations`)
- **Status:** Evaluated and Discarded.
- **Methodology:** We established the **Two-Way Validation Principle**: all algorithms must pass both Math SNR (Gate A) and Live LLM Generation (Gate B).
- **Findings:** We tested Percentile Clipping, Block/Group Quant (G=32), and Sparse-Dense Hybrids against the Qwen 0.5B model.
- **Verdict:** While the Sparse-Dense hybrid scored an incredible 41.23 dB in raw mathematical SNR, it catastrophically failed the live text generation test (broken grammar/hallucinations). Extracting outliers into sparse matrices breaks the model's structural timing (e.g., RoPE).
- **Architectural Decision:** Dense rotation (TurboQuant) combined with a 1-Bit QJL residual is the officially verified, superior path for Edge AI A4A4 quantization.

---

## Global Next Steps
1. **Pillar 2.2:** Scaffold 1.58-bit (Ternary) and 1-bit (Binary) MAC prototypes to explore total elimination of floating-point multipliers.
2. **Pillar 1:** Write the Metal shader kernels for the Mamba block-parallel scan.