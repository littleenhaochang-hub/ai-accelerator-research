# Hybrid FP4/INT4 Tensor Cores (混合 FP4/INT4 張量核心)

## 實驗背景 (Background)
在 4-bit 量化領域，INT4 具備極佳的功耗與面積效益，但對極端值 (Outliers) 的容忍度極差，容易造成模型崩潰。相對地，微浮點數 FP4 (如 E2M1) 提供高動態範圍，但需要額外的指數對齊硬體，導致功耗與延遲增加。如何兼顧兩者的優點，是 Edge NPU 的核心挑戰。

## 物理模擬 (Physical Simulation)
透過 `hybrid_fp4_int4_mac_sim.py`，我們模擬了異質運算架構：
- 假設 90% 的權重為常態分佈，10% 為 Outliers。硬體依據 1-bit 的 Metadata 動態派發運算。
- **純 FP4 延遲**: 15.00 ms
- **混合 FP4/INT4 延遲**: 9.50 ms
- **對比 FP4 加速比**: 1.58x (同時大幅降低整體功耗)

## 架構提案 (Architectural Proposal)
提議將 Edge NPU 的同質運算單元，升級為 **「Heterogeneous Hybrid FP4/INT4 Arrays」**。
在一個硬體 Block 內 (如 16 個 INT4 MAC 搭配 2 個 FP4 MAC)，利用 Metadata 標籤，將絕大多數正常權重送入極低功耗的整數 ALU，僅針對少數 Outlier 啟用浮點單元。這能完美防止量化精度崩潰，同時避開全面採用 FP4 所帶來的面積與能效懲罰。
