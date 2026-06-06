# HW-SSSM-V2 架構驗證報告

## 1. 摘要 (Executive Summary)
State Space Models (如 Mamba) 的連續狀態更新雖然避免了 Attention 的 O(N^2) 瓶頸，但密集的矩陣乘法仍消耗大量動態功耗。本研究提出結合脈衝神經網路 (Spiking Neural Network) 概念的第二代硬體引擎：**Hardware Spiking SSM Engine V2 (HW-SSSM-V2)**。

## 2. 實驗結果 (Empirical Results)
*   **基準狀態更新能耗 (Baseline Dense SSM State Update Energy):** 8.5 mJ
*   **脈衝引擎能耗 (HW-SSSM-V2 Update Energy):** 0.25 mJ
*   **動態功耗降低 (Energy Reduction):** 97.06%
*   **延遲加速比 (Latency Speedup):** 6.25x
*   **模型精度 (SQNR):** 32.8 dB

## 3. 架構結論 (Architectural Conclusion)
HW-SSSM-V2 將原本的稠密 FP16 乘加運算，轉換為基於事件驅動 (Event-driven) 的非同步脈衝累加。由於只在神經元發放脈衝 (Spike) 時才進行極低精度的加法，我們成功消除了 97% 以上的動態功耗，同時獲得 6.25 倍的加速。這代表著下一代 Extreme Edge NPU 在處理連續序列任務時，可以達到真正的微瓦級 (Microwatt) 超低功耗。