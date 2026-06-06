# 硬體上下文感知 Token 截斷器 (HW-CATT)

## 摘要
為解決 Edge Agentic AI (如 Mac mini 本地執行) 面臨的長文本 Prefill OOM (Out of Memory) 與延遲爆炸問題，我們探索了硬體層級的 Context-Aware Token Truncator (HW-CATT)。

## 實驗設計
*   **瓶頸分析:** 當輸入 Token 超過 32K (例如未截斷的 HTML DOM) 時，軟體層級的排序與截斷會帶來大量的 CPU-Memory 往返延遲。
*   **硬體架構:** 引入 HW-CATT，將上下文過濾邏輯 (如 HTML 標籤精簡、無效 CSS 移除) 實作為 SRAM 寫入埠之前的行內 (Inline) 過濾器。
*   **參數:** 輸入 128,000 tokens，目標保留 4,096 tokens 的高密度資訊。

## 實驗結果
*   **軟體截斷延遲:** 857.16 ms
*   **HW-CATT 延遲:** 25.60 ms
*   **吞吐量加速:** **33.48 倍**

## 架構結論
要在 Edge 裝置上運行 Agentic AI，將海量無結構文本 (如 Web DOM) 在送入 LLM Attention 矩陣前進行硬體級截斷是不可或缺的。HW-CATT 能以 Zero-MAC 的代價，實現 33.48x 的延遲縮減，徹底解決長文本引發的 Prefill 瓶頸。建議將此模組整合進未來的 Edge NPU Ingress DMA 中。