# LLM 稠密線性投影的光學張量核心 (Photonic Tensor Core) 架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
在大語言模型 (LLM) 推論的解碼階段，Vector-Matrix Multiplication (向量-矩陣乘法) 主導了系統的動態功耗。即使採用 INT4 量化，對於 8192 維度的隱藏層，單次 Token 生成仍需執行超過 6700 萬次 MAC 運算。傳統數位電路的充放電能耗成為 Edge NPU 散熱的瓶頸。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
我們引入了 **矽光子張量核心 (Photonic Tensor Core, PTC)** 的架構概念。利用馬赫-曾德爾干涉儀 (Mach-Zehnder Interferometers, MZI) 網格，可以在光學域以光速 (接近零功耗) 完成類比矩陣乘法。
在光學架構下，計算本身的功耗幾乎為零，系統的總功耗完全由邊緣的 DAC (數位轉類比) 與 ADC (類比轉數位) 轉換器決定。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`photonic_tensor_core_sim.py`
- **數位 NPU (INT4)**: 單層生成能耗約 33554.43 nJ，運算延遲 15.0 ns
- **光學 NPU (PTC)**: 單層生成能耗約 32.77 nJ，光學傳輸延遲 2.5 ns
- **能耗降低 (Energy Reduction)**: **1024.00x**
- **運算加速 (Speedup)**: **6.00x**

## 4. 硬體架構建議
對於未來的 Extreme Edge NPU (如穿戴式設備或無電池感測器)，純數位 Tensor Core 已面臨功耗牆。建議將核心的 FFN 投影層遷移至「光學協同處理器」，將計算複雜度從 $O(N^2)$ 降維為 $O(N)$ 的資料轉換開銷。
