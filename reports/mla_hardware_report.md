# Auto-Researcher 報告: DeepSeek MLA (Multi-Head Latent Attention) 硬體即時投影架構

## 摘要
傳統的 Multi-Head Attention (MHA) 甚至 Grouped-Query Attention (GQA) 在長文本推論時，KV Cache 的記憶體頻寬 (Memory Bandwidth) 消耗極大。DeepSeek 的 MLA 架構透過將 KV Cache 壓縮為一個低維度的 Latent Vector，在推論時動態投影回 K 與 V。本實驗模擬此架構在 Edge NPU 上的記憶體頻寬節省。

## 實驗設定
- 序列長度: 2048 tokens
- 完整維度 (Full Dim): 4096
- 潛在維度 (Latent Dim): 512

## 模擬結果
* **Baseline (MHA) KV Cache 讀取量:** 32,768.00 KB / Step
* **Proposed (MLA) Latent Cache 讀取量:** 2,048.00 KB / Step
* **記憶體頻寬節省 (Bandwidth Reduction):** 93.75%

## 結論與架構建議
透過 MLA 架構，推論時的 Memory Wall 瓶頸可大幅舒緩。然而，Latent Vector 動態還原為 K, V 需要極大的即時矩陣運算 (Up-projection)。強烈建議在下一代 NPU 的 SRAM 旁直接整合 **On-the-fly Projection Engine**。將 Up-projection 權重常駐於 NPU 的 L2 Cache 內，當 Latent Vector 從 DRAM 載入時，硬體 Pipeline 即時將其還原並直接送入 Tensor Core 進行 Attention 計算，完全不將還原後的 K, V 寫回主記憶體，以達到 93.75% 的極致頻寬節約。
