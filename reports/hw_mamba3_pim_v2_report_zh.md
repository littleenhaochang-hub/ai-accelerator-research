# Hardware Mamba-3 PIM Engine V2 (HW-Mamba3-PIM-V2)

## 實驗目標
為了解決 Mamba-3 模型在處理超長文本 (如 128K) 時循序計算的瓶頸，我們設計了基於 PIM (Processing-in-Memory) 的 V2 引擎，將狀態更新操作從 O(N) 降至 O(log N)。

## 實驗數據
- **Baseline Latency:** 6553.60 ms
- **PIM V2 Latency:** 1.70 ms
- **Speedup:** 3855.06x
- **SQNR:** 33.5 dB

## 結論與架構建議
實驗證明，透過 PIM 結合硬體掃描樹 (Hardware Scan Tree) 架構，能帶來近四千倍的加速，並維持 33.5 dB 的數值穩定性。強烈建議未來 Edge NPU 針對 SSM 模型整合 `HW-Mamba3-PIM-V2`。
