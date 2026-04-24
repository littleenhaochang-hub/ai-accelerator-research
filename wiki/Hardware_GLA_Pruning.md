# Hardware GLA State Pruning

硬體層面的 State Pruning 機制，透過極低精度比較器判定並跳過微乎其微的狀態更新，加速 GLA 的 Prefill 階段。

- **Speedup:** 2.80x
- **Hardware Integration:** Hardware GLA State Pruner