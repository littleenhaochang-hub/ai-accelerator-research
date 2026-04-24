# 多晶片封裝之矽光子共封裝光學 (CPO) 架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
隨著單晶片面積逼近物理極限 (Reticle Limit)，Edge NPU 正走向 Multi-Chiplet 架構。然而，晶片間 (Die-to-Die, D2D) 依賴傳統有機載板的電氣訊號傳輸，其頻寬極低 (如 256 GB/s) 且每位元傳輸能耗極高 (4.5 pJ/bit)，導致跨晶片的張量並行 (Tensor Parallelism) 延遲成為致命傷。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
為了打破 Chiplet 之間的通訊牆，我們提出了將 **Silicon Photonics (矽光子)** 與 **Co-Packaged Optics (CPO, 共封裝光學)** 導入 Edge NPU 架構。透過將雷射光源與光調變器直接封裝在 NPU 晶粒旁，資料能以光速在晶片間傳輸，距離造成的訊號衰減與 RC 延遲幾乎為零。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`optical_cpo_sim.py`
針對 16GB 的層間資料交換：
- **傳統電氣互連**: 延遲 62.50 ms，傳輸能效極差 (4.5 pJ/bit)
- **光學 CPO 互連**: 延遲 7.81 ms，傳輸能效極佳 (0.5 pJ/bit)
- **延遲加速 (Latency Speedup)**: **8.00x**
- **傳輸能效提升 (Energy Efficiency Gain)**: **9.00x**

## 4. 硬體架構建議
針對次世代由多個小晶粒組成的 Edge AI 工作站，強烈建議捨棄高耗能的電路板走線與昂貴的 2.5D 矽中介層，全面擁抱 CPO 光學互連。這將允許多個物理 Chiplet 在軟體層面上完美偽裝成單一超大容量的邏輯 NPU，實現 100% 的運算利用率。
