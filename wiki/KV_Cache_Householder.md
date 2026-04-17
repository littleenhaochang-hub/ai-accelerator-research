# KV Cache 4-bit TurboQuant Householder Simulation

## 實驗背景
根據 MEMORY.md 的架構藍圖，Edge 推論長文本 (32K+ tokens) 最大的瓶頸在於 KV Cache 佔用與量化時的運算開銷。TurboQuant 採用隨機正交矩陣來消除 Activation Outliers，但 $O(N^2)$ 的編碼過程會導致 Prefill 效能崩潰。

## 硬體模擬與分析
- **腳本**: `kv_householder_sim.py`
- 以 Seq Length 32K, Head Dim 128 為例，傳統矩陣相乘需要 5.24 億次 MACs。
- **Chained Householder Reflections**: 改用 $k=4$ 的反射鏈，複雜度降至 $O(k \cdot N)$，MACs 下降至 1638 萬次。
- **硬體加速比**: 32.0x (降低運算負擔 32 倍)。

## 架構協同設計結論
未來的 Edge NPU (如 M-series) 應在 Attention / KV-Cache SRAM 旁整合專屬的 Householder SIMD 向量運算單元。這能達到 Zero-Overhead 的 4-bit KV Cache Encoding，消除 Prefill 的 ALU 瓶頸。
