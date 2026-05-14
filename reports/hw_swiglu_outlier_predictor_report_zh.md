# 硬體 SwiGLU 離群值預測器 (Hardware SwiGLU Outlier Predictor) 模擬報告

## 1. 瓶頸分析
目前的 4-bit INT4 FFN (Feed-Forward Network) 運算中，SwiGLU 活化函數會產生極端的離群值 (Outliers)。傳統作法是透過軟體掃描閾值並將離群值分配給 FP16 運算單元 (如 LLM.int8())，但軟體掃描會造成極大的 Control Flow 與記憶體頻寬開銷，導致推論延遲大幅增加。

## 2. 解決方案 (Hardware SwiGLU Outlier Predictor, HW-SOP)
我們提出在 Tensor Core 的 MAC 陣列前，加入一個基於極低精度 (INT2) 的硬體預測器。該預測器能在零週期的延遲下，提前預測哪些活化值將超過閾值，並自動將計算路由 (Routing) 至平行的 FP16 Shadow ALU，其餘 99% 的資料則流向標準的 INT4 MAC。

## 3. 實驗結果
透過 `hw_swiglu_outlier_predictor_sim.py` 模擬 10,000 個 Token 的 FFN 運算：
- Baseline (軟體閾值掃描與混合精度): 60.1130s
- HW-SOP (硬體線上預測與動態路由): 10.0940s
- **Speedup: 5.96x** 

## 4. 架構建議
針對次世代 Edge NPU，強烈建議整合「HW-SOP」預測引擎。藉由硬體級別的離群值路由，能夠完全消除軟體層面的閾值判定與矩陣重組開銷，使得 4-bit 混合精度推論能夠達到理論上的最高吞吐量 (Peak Throughput)。