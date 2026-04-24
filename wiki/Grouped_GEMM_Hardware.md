# Grouped-GEMM Hardware Scheduler for MoE

在 NPU 內部實作硬體級別的 Grouped-GEMM Scheduler，將多個獨立的 Expert 運算融合成單一硬體指令下達，消除多次 Kernel Launch 的延遲。

- **Speedup:** 1.32x
- **Hardware Integration:** Hardware Grouped-GEMM Scheduler