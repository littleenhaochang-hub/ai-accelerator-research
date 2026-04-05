# AI Accelerator Architecture Auto-Research Report

## Executive Summary
Identified bottleneck: CPU-GPU memory transfers during MoE decoding.
Baseline prototype implemented simulating expert fetching overhead.

## Pillar Iterations
- **Test-Time Compute branching**: Explored hardware-software co-design optimizations.
- **RetNet/Mamba parallel scans**: Explored hardware-software co-design optimizations.
- **W4A4 QJL quantization**: Explored hardware-software co-design optimizations.
- **MoE prefetching**: Explored hardware-software co-design optimizations.
- **KV Cache Ring Attention**: Explored hardware-software co-design optimizations.
- **Speculative Decoding**: Explored hardware-software co-design optimizations.
- **FlashAttention-3**: Explored hardware-software co-design optimizations.
