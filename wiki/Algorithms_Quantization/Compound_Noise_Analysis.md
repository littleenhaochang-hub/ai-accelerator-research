# Universal Benchmark (Compound Noise Analysis)

Evaluates the destructive compounding effect of Quantization Noise + Accumulator Truncation.

## Qwen2.5-1.5B Target Architecture Results
| Config | PPL | Verdict |
| :--- | :--- | :--- |
| W16_A16 + FP32 Acc | 6.650 | Baseline |
| W8_A8 (Sub-channel) + FP24 Acc | 7.543 | Safe (Industry Standard) |
| W4_A4 (Linear) + FP24 Acc | 30.056 | Failed (Catastrophic) |
| **W4_A4 (NF4 LUT + Householder) + FP24 Acc** | **9.390** | **Edge Tape-out Target** |

*Methodology: Sub-channel quantization applied in blocks of 128 elements. Global accumulation truncated to FP24 per chunk of 32.*
