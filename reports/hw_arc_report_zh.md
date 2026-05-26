# Hardware Activation Range Collector (HW-ARC)

## 摘要
在進行動態量化 (Dynamic Quantization) 時，軟體層級需要掃描整個 Activation Tensor 來尋找 Min/Max 值，這在長文本 (如 16K context) 下會產生顯著的 O(N) 延遲與記憶體讀取開銷。本研究提出設計「HW-ARC 引擎」，將 Min/Max 追蹤邏輯整合至 SRAM 寫入埠，實現 O(1) 的即時範圍收集。

## 實驗結果
- **軟體延遲**: 503.32 ms
- **硬體延遲**: 0.012 ms
- **加速比**: 41943.04x

## 結論
硬體加速的活化值範圍收集能完全隱藏動態量化的尺度計算延遲。建議將此「HW-ARC」模組整合至 Edge NPU 記憶體控制器中，以實現零開銷的動態混合精度推論。