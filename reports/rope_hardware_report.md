# RoPE (Rotary Position Embedding) CORDIC 硬體加速分析

## 實驗背景
在處理極長文本 (例如 32K Context) 時，旋轉位置編碼 (RoPE) 的記憶體開銷變得極為巨大。在純軟體實現中，通常需要預先計算並儲存龐大的 sin/cos 矩陣 (RoPE Cache)。在每一次 Attention 運算前，硬體必須從 DRAM 讀取這些 Cache 並執行複數乘法，這會消耗大量記憶體頻寬。

## 實驗方法
撰寫 `rope_hardware_sim.py`，模擬 32K Context 下 RoPE 的記憶體讀取與運算延遲，並評估整合專用 CORDIC 引擎的硬體效益。

## 實驗數據
- **Context Length**: 32,768 tokens
- **Software RoPE Cache Size**: 536.87 MB
- **Software RoPE Latency**: 3605.98 us (主要為記憶體頻寬瓶頸)
- **Hardware RoPE Latency**: 0.00 us (完全隱藏於 Pipeline 中)

## 硬體架構結論
對於長文本推論，預計算的 RoPE Cache 會佔用高達 536MB 的記憶體，並帶來超過 3.5ms 的延遲。
為了徹底解決此問題，未來的 Edge NPU 必須在 SRAM 的讀取埠 (Read Port) 旁整合專用的 **CORDIC RoPE Engine (基於 CORDIC 演算法的 RoPE 引擎)**。透過該引擎，硬體能在 Q / K Tensor 從 SRAM 取出的同一個 Clock Cycle 內，on-the-fly 算出 sin/cos 並完成旋轉。這將 100% 消除 RoPE Cache 的記憶體佔用與頻寬消耗。
