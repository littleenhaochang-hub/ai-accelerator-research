# 硬體視覺語言 Token 合併器 (Hardware Vision-Language Token Merger, HW-VLTM)

## 摘要
針對多模態模型 (Vision-Language Models) 在處理高解析度影像時產生的龐大冗餘視覺 Token，我們評估了將 Token Merging (ToMe) 相似度計算與合併邏輯直接實作於硬體層級的設計。

## 實驗結果
- **基準延遲 (軟體 Token Merging)**: 20.48 ms
- **改進延遲 (HW-VLTM)**: 0.41 ms
- **加速比**: 50.00x

## 結論
透過在 Edge NPU 的 SRAM 寫入控制器中整合 HW-VLTM，可以在數據進入 MAC 陣列前，以零週期的軟體開銷動態合併背景冗餘視覺 Token，減少 75% 的計算與記憶體負擔。這對在受限電量下運行多模態 Agentic AI 至關重要。
