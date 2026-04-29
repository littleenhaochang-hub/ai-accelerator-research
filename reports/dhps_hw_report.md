# 實驗報告：Dynamic Hardware Precision Scaling (DHPS)

## 背景 (Background)
在邊緣裝置上，目前主流的作法是將 LLM 權重與 KV Cache 靜態量化至 INT4。然而，並非所有 Token 對生成結果的貢獻度都相同。強制將所有狀態保留在 INT4 浪費了大量記憶體頻寬與運算週期。

## 方法 (Methodology)
本實驗引入 **Dynamic Hardware Precision Scaling (DHPS)**，在 NPU 中嵌入「硬體級別的精度動態分配器」。系統根據 Attention 權重動態分配精度：
- 關鍵 Token (10%) 使用 INT8 保留細節。
- 一般 Token (30%) 維持 INT4。
- 背景/長尾 Token (60%) 極限壓縮至 INT2。
所有精度切換由硬體 Router 於 Cycle 級別無縫調度，免除軟體 Control Flow 的嚴重延遲。

## 驗證結果 (Results)
- **基準靜態 INT4 延遲 (Baseline):** 0.4350 秒，平均 4 Bits/Token。
- **DHPS 動態精度延遲 (Proposed):** 0.2746 秒，平均 3.20 Bits/Token。
- **整體提升:** 混合精度硬體調度將整體延遲降低，吞吐量提升達 **1.58x**，並進一步將 KV Cache 的平均記憶體足跡壓縮至 3.2 Bits/Token。

## 物理架構建議 (Architectural Proposal)
建議在 Edge NPU 內部實作「Multi-Precision MAC Arrays (支援 INT2/4/8 切換)」與「Inline Precision Router」。硬體必須能在讀取 SRAM 的當下，根據 Metadata 即刻選擇對應的解壓縮與 MAC 通道，達成零等待的動態精度推論。
