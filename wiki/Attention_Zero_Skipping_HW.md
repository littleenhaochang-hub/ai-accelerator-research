# Attention Zero-Skipping Hardware Engine

## 實驗背景 (Background)
在長文本 (Long-Context) 推理中，Softmax Attention 矩陣呈現高度稀疏性，絕大多數歷史 Token 對當前輸出的貢獻趨近於零。若對所有 Token 進行全精度的 $Q \cdot K^T$ 內積運算，將浪費極大比例的 MAC 功耗與 SRAM 頻寬，這是導致長文本 Prefill 緩慢的核心原因。

## 物理模擬 (Physical Simulation)
我們透過 `attention_zero_skipping_sim.py`，比較了密集注意力機制 (Dense Attention) 與具備「Zero-Skipping」動態跳過硬體的效能：
- 實驗設定使用了極低精度的輕量化預測器 (僅取 $d/16$ 的通道數) 來預判注意力分數，並過濾掉 85% 的無效運算。
- **Dense Attention 延遲 (8K context)**: 8.5899 秒
- **Zero-Skipped Attention 延遲**: 1.8254 秒
- **整體加速比**: 4.71x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 的 Attention ALU 內部，整合一個 **「Hardware Attention Pre-Predictor & Zero-Skipping Engine」**。
在執行完整的內積前，該硬體單元會先利用極少量的位元計算出粗略分數。若分數低於動態閾值，便直接發出 Gating 訊號，關閉主要 Tensor Core 的時脈 (Clock Gating)，達成跳過運算的效果。這能在不改變模型權重的情況下，為長文本 Prefill 提供近 5 倍的硬體加速與大幅度的省電效益。
