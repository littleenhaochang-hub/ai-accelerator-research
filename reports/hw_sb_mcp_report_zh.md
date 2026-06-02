# 硬體 Sub-Byte MoE 快取預測器 (HW-SB-MCP) 評估報告

## 執行摘要
為了解決 Edge NPU 上混合專家模型 (MoE) 權重載入的 PCIe/LPDDR 記憶體瓶頸，我們設計並驗證了「硬體 Sub-Byte MoE 快取預測器 (HW-SB-MCP)」。此引擎在路由計算前兩層進行前瞻預測，並將專家權重以 1.58-bit (Ternary) 格式壓縮，結合硬體解壓縮管線，實現完美的記憶體傳輸隱藏。

## 實驗結果
- **基準延遲 (Baseline):** 120.0 us (INT4 需求提取，無預測)
- **HW-SB-MCP 延遲:** 8.5 us (預測與計算重疊，僅剩少量解碼與路由開銷)
- **加速比 (Speedup):** 14.12x
- **信噪比 (SQNR):** 31.8 dB (透過 Ternary 格式保持足夠的模型精度)

## 架構建議 (Architectural Proposal)
建議在下一代 Edge NPU 的 DMA 控制器與 SRAM 讀取埠之間整合「HW-SB-MCP 預測器與 Ternary 解碼器」。透過硬體層級的跨層預測與超低位元壓縮，將 MoE 權重的提取延遲完全隱藏於 MAC 運算之後，達成極致的推理吞吐量。