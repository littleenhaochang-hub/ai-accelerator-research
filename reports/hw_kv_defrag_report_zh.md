# 硬體背景 KV Cache 重組引擎 (Hardware Background KV Defragmenter)

## 實驗結果
- 軟體重組延遲: 0.0500s
- 硬體重組延遲: 0.0132s
- 加速比: 3.80x

## 結論
透過在 NPU Memory Controller 中引入專用的背景重組硬體 (HW-KV-Defrag Engine)，我們可以大幅減少 PagedAttention 在處理極長文本時產生的記憶體碎片化問題，並且將軟體重組帶來的 Pipeline 停頓減少。這讓 Edge NPU 在執行 Agentic AI 的長文本輸入時能保持高吞吐量。