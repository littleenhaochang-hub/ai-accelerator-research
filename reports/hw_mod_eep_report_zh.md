# Hardware MoD Early Exit Predictor (HW-MoD-EEP) 實驗報告

## 摘要 (Executive Summary)
Mixture-of-Depths (MoD) 架構透過跳過不重要的 Token 來節省算力。但在軟體端計算 Capacity Router 並排序 Token 會產生顯著的延遲。本實驗評估將 MoD 路由閾值判斷轉移至硬體的「硬體 MoD 提早退出預測器 (HW-MoD-EEP)」。

## 實驗結果
- **Software Routing Latency**: ~0.04 ms
- **HW-MoD-EEP Latency**: ~0.003 ms
- **Speedup**: 12.32x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過硬體層級的平行比較器陣列，可以完全隱藏 MoD 路由的排序與選擇延遲。我們建議在 Edge NPU 的排程器中整合「HW-MoD-EEP 引擎」，使得不重要的 Token 能在進入 MAC 陣列前被零週期 (Zero-cycle) 丟棄，大幅提升生成速度。
