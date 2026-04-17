# On-Device PEFT (LoRA) Hardware Simulation Report
## 背景 (Background)
Edge AI 逐漸走向在地化學習 (On-Device Learning)。微調 LLM 最常用的 LoRA (Low-Rank Adaptation) 在合併權重 ($W = W_0 + \Delta W$) 時，傳統架構會產生巨量的 CPU-DRAM 往返傳輸。

## 模擬參數 (Parameters)
- Hidden Dimension: 4096
- LoRA Rank: 16
- W0 Size: 32.0 MB
- LoRA Weights Size: 256.0 KB

## 模擬結果 (Results)
- 傳統 CPU-DRAM 權重更新能耗: 642.50 µJ
- Pure In-SRAM (NPU 內部更新) 能耗: 6.48 µJ
- 能源效率提升: 99.23x

## 架構建議 (Architectural Proposal)
新一代 Edge NPU 必須包含 **In-SRAM Gradient Aggregator (SRAM 內梯度聚合器)**。這允許在 NPU 內部直接計算 $\Delta W = A 	imes B$ 並直接與 SRAM 中的 $W_0$ 進行 In-Place Addition，完全繞過耗電的 CPU 與 DRAM 匯流排。這對於依賴電池的行動裝置執行 Federated Learning 或 Personalization 微調至關重要。
