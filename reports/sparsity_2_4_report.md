# 2:4 Structured Sparsity 邊緣硬體加速架構研究報告

## 研究背景與瓶頸
在 Edge AI (如 Mac mini, 專用 NPU) 部署大規模語言模型時，運算單元 (MACs) 與記憶體頻寬常常達到物理極限。N:M 結構化稀疏 (Structured Sparsity) 被提出來在不顯著影響模型精度的前提下減少運算量。其中 2:4 稀疏度 (每 4 個權重保留 2 個) 由於與 Tensor Core 的硬體架構高度契合，成為最具潛力的方向。

## 原型設計 (Prototype)
我們在 `sparsity_2_4_sim.py` 中建立了一個硬體與軟體協同設計的模擬：
* **Model Architecture:** 使用 2:4 結構化稀疏修剪權重，並保留非零權重的元資料 (Metadata/Indices)。
* **Hardware Architecture:** 模擬支援 Sparse Tensor Core 的硬體。硬體讀取權重時，透過 Metadata 進行多工器 (MUX) 選擇，將對應的 Activation 載入 MAC 陣列，跳過零值的運算。

## 實驗結果與數據
數學分析與理論模擬顯示：
* 對於標準的矩陣乘法，運算量 (MACs) 直接減半。
* **記憶體頻寬降低 (Bandwidth Reduction):** 傳統 Dense 16-bit 權重每 4 個佔用 8 bytes。2:4 稀疏化後，只需儲存 2 個 16-bit 權重 (4 bytes) 以及 2-bit 的 Metadata (0.5 bytes)，總共 4.5 bytes。頻寬消耗降低了 **43.75%**。
* **效能提升 (Speedup):** 理論上，若 Sparse MAC 陣列利用率達到 100%，運算週期將縮短一半，達成 **2.0x** 運算加速。

## 結論
2:4 結構化稀疏不僅能提供 2 倍的運算吞吐量提升，更能減少近 44% 的記憶體頻寬需求，這對於 Memory-Bound 的 LLM 推論至關重要。建議在下一代 NPU 的微架構設計中，原生加入 Sparse Tensor Core 以及硬體 Metadata 解碼器，以最大化稀疏化模型的效能。
