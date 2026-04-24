# Mamba-2 Hardware State Caching

在 NPU 內建專用的 SRAM 區塊作為 Mamba State Cache，避免與一般快取競爭並支援單週期更新。

- **Speedup:** 30.00x
- **Hardware Integration:** Dedicated Mamba State Cache