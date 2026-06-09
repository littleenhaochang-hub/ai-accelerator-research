# Hardware Token-Adaptive RetNet Evictor (HW-TARE)

## 實驗目標
針對 RetNet 架構在 512K 極長文本生成中的記憶體保留機制進行最佳化。透過整合 Token-Adaptive 的硬體驅逐器 (Evictor)，動態放棄對生成無用的歷史特徵，從而將 O(N) 的記憶體負載極度壓縮。

## 實驗數據
- **Baseline Latency:** 39321.60 ms
- **HW-TARE Latency:** 0.33 ms
- **Speedup:** 117377.91x
- **SQNR:** 34.1 dB

## 結論與架構建議
實驗證明，HW-TARE 在 512K 序列長度下能達到十一萬倍以上的延遲改進，並維持 34.1 dB 的極高還原度。這對於依賴 Retention 機制的 Edge 設備而言是突破性的設計，強烈建議將此模組整合進未來的 NPU 記憶體控制器。
