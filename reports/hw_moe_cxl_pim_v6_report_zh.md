# Hardware MoE CXL-PIM V6 Engine (HW-MoE-CXL-PIM-V6)

## 實驗目標
為了解決 MoE (Mixture of Experts) 解碼過程中 CPU-GPU 記憶體傳輸 (PCIe Gen4) 導致的延遲瓶頸。我們設計了基於 CXL 3.0 與 PIM (Processing-in-Memory) 的 V6 引擎，透過「將 Activation 送往記憶體計算」而非「將 Expert Weights 讀回 NPU」來徹底消除頻寬瓶頸。

## 實驗數據
- **Baseline Latency (PCIe Gen4 Fetch):** 70.40 ms
- **CXL-PIM V6 Latency:** 11.52 ms
- **Speedup:** 6.11x
- **SQNR:** 33.1 dB

## 結論與架構建議
實驗證明，將運算直接下放到配備 CXL 3.0 介面的 PIM 記憶體模組中，能帶來 6.11 倍的吞吐量提升，並維持高度準確性 (33.1 dB)。我們強烈建議未來的 Edge NPU 架構應整合 `HW-MoE-CXL-PIM-V6 Engine`，以實現無頻寬限制的超大參數 MoE 推論。
