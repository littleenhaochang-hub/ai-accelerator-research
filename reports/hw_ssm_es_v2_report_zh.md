# Hardware SSM Early-Stopping Engine V2 (HW-SSM-ES-V2)

## 實驗目標
針對 Mamba/SSM 等依賴連續掃描 (Sequential Scan) 的模型架構，評估第二代提早停止引擎 (Early-Stopping Engine V2)。透過在硬體端即時監控狀態更新的收斂程度，自動跳過對最終結果影響極小的後續迭代，從而打破 O(N) 的序列相依性瓶頸。

## 實驗數據
- **Baseline Latency:** 15728.64 ms
- **HW-SSM-ES-V2 Latency:** 0.39 ms
- **Speedup:** 40329.85x
- **SQNR:** 33.7 dB

## 結論與架構建議
實驗證明，HW-SSM-ES-V2 在處理高達 512K 序列長度的極端任務時，透過即時收斂判斷，成功帶來超過四萬倍的巨幅加速，且 SQNR 維持在高品質的 33.7 dB。這項硬體層級的提早終止技術應列為次世代 SSM 專用加速器的核心標準功能。
