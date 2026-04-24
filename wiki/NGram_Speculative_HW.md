# Hardware N-Gram Speculative Decoding

## 實驗背景 (Background)
傳統的 Speculative Decoding (推測解碼) 依賴小型的 Draft Model 來進行 Token 預測。然而在邊緣運算 (Edge NPU) 中，即便是小模型也會消耗可觀的記憶體頻寬與 MAC 運算資源。最新的 arXiv 研究指出，針對特定任務 (例如程式碼生成或 DOM 結構解析)，局部上下文的 N-gram 統計已經足以提供高接受率的 Draft Token。

## 物理模擬 (Physical Simulation)
我們透過 `ngram_speculative_hw_sim.py`，比較了 1B Draft Model 與硬體 SRAM N-gram Cache 的延遲：
- **Draft Model 延遲 (2048 Tokens)**: 30.72 ms
- **SRAM N-Gram 硬體查找延遲**: 2.05 ms
- **整體加速比**: 15.00x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 SRAM 控制器旁加裝 **「Hardware N-Gram Cache Tracker」**。
在模型進行 Prefill 與 Decode 時，該硬體單元會自動在背景建立當前 Context 的 N-gram 轉移機率表。在需要 Draft Token 時，它能在 1 個 Clock Cycle 內提供高機率預測值給主模型進行驗證，實現真正的「零 MAC 開銷」推測解碼，徹底釋放 Edge NPU 的運算能力。
