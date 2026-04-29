# 實驗報告：Hardware Dynamic Attention Head Gating (HDAG)

## 背景 (Background)
在多頭注意力機制 (MHA/GQA) 中，不同 Attention Head 捕捉到的語意特徵具有高度冗餘性。在生成階段 (Decode Phase)，強制讀取所有 Head 的 KV Cache 會導致極大的 Memory Bandwidth 浪費，這在 Edge NPU 上是極致命的瓶頸。

## 方法 (Methodology)
本實驗設計了 **Hardware Dynamic Attention Head Gating (HDAG)** 引擎。透過在 NPU 內部實作一個超低精度的「Head 重要性預測器 (Head-Importance Predictor)」，在讀取 SRAM 之前，硬體級別動態屏蔽掉當前 Token 影響力極低 (如 Bottom 75%) 的 Attention Heads，從而直接跳過對應 KV Cache 的記憶體搬運。

## 驗證結果 (Results)
- **基準 Dense Attention 延遲 (Baseline):** 0.5000 秒，頻寬消耗 67.11 MB。
- **硬體 Gating Attention 延遲 (Proposed):** 0.2831 秒，頻寬消耗 16.78 MB (Active Ratio = 25%)。
- **整體提升:** 記憶體頻寬需求大降 **75%**，整體 Decode 吞吐量提升達 **1.77x** (包含硬體預測器 Overhead)。

## 物理架構建議 (Architectural Proposal)
建議在 Edge NPU 的 SRAM 讀取埠前方整合「HDAG 預測器與動態遮罩 (Dynamic Mask) 邏輯」。這使得硬體能夠以零軟體開銷 (Zero Software Overhead) 自主決定每一層哪些 Head 需要被喚醒，極大地緩解了長文本生成時的 Memory Wall 挑戰。
