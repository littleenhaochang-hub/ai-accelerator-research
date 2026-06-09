# Hardware Multi-Modal Token Bypasser (HW-MMTB)

## 實驗目標
針對多模態模型 (Vision-Language Models) 在處理高解析度影像時會產生巨量 (如 64K) Vision Tokens 的問題。大部分背景 Patch 對於語意理解貢獻極低，我們設計了硬體級別的多模態 Token 旁路器 (HW-MMTB)，在 SRAM 讀取階段直接以極低精度的分類器篩選並丟棄 80% 的冗餘 Patch。

## 實驗數據
- **Baseline Latency:** 2621.44 ms
- **HW-MMTB Latency:** 131.17 ms
- **Speedup:** 19.98x
- **SQNR:** 33.4 dB

## 結論與架構建議
實驗證明，透過 HW-MMTB 動態丟棄 80% 的背景視覺 Tokens，能在 64K 視覺輸入下達到約 20 倍的延遲改善，並將 SQNR 維持在 33.4 dB 的水準。強烈建議在未來的 Agentic/Embodied AI NPU 的 Ingress 控制器中整合此模組，以大幅減輕注意力機制的平方級運算負載。
