# Universal Hardware Benchmark Suite (Compound Noise Evaluation)

## Objective
Evaluate the compounding noise effects of extremely low-bit quantization (INT8/INT4) combined with reduced-precision global accumulators (FP24). This benchmark proves whether the Edge Tape-out architectures can survive the physical truncation error introduced by replacing FP32 global accumulators with FP24.

## Experimental Matrix

### Dimension 1: Module Coverage
- Full Model Replacement (Attention Q,K,V,O + FFN Gate,Up,Down)

### Dimension 2: Hardware Dataflow Configurations
1. **W16_A16 + FP32 Acc:** Pure software baseline (BF16).
2. **W8_A8 (Per-Tensor) + FP24 Acc:** Negative control. Naive quantization + FP24 Acc (Chunk 32). Expected to fail catastrophically due to outliers.
3. **W8_A8 (Sub-channel B128) + FP24 Acc:** Industry standard. e8m0 block scaling with FP24 accumulation.
4. **W4_A4 (Sub-channel Linear B128) + FP24 Acc:** High compression linear baseline.
5. **W4_A4 (NF4 LUT + Householder TurboQuant) + FP24 Acc:** The Edge Tape-out Target. Sub-4-bit with mathematically optimal NF4 mapping, evaluated alongside FP24 truncation.

### Dimension 3: Benchmark Datasets
1. **WikiText-2 (Validation):** Basic linguistic grammar and short-range dependency.
2. **Penn Treebank (PTB):** Strict structural syntax and vocabulary.

## Methodology
The simulation maps the fake-quantized tensors through a vectorized FP24 chunked accumulator. Since the Block Size (128) is a multiple of the Accumulator Chunk Size (32), the simulation mathematically matches the physical silicon behavior of local INT32 accumulation -> scale application -> global FP24 reduction.
