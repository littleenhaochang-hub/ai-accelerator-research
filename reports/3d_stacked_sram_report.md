# 3D 堆疊 SRAM (SRAM-on-Logic) 解決超大 KV Cache 瓶頸研究

## 1. 瓶頸分析 (Bottleneck Analysis)
隨著 LLM 上下文長度突破 128K，單層的 KV Cache 容量需求飆升至數 GB。傳統 2D 平面 (Planar) SRAM 若要提供如此大的容量，晶片面積將極度膨脹，導致嚴重的水平金屬導線 RC 延遲 (Wire Delay)，存取延遲高達 45ns，抵銷了 SRAM 的速度優勢。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
我們引入了 **3D 堆疊 SRAM (SRAM-on-Logic)** 架構，透過混合鍵合 (Hybrid Bonding) 技術與矽穿孔 (TSV)，將超大容量的 SRAM 直接垂直堆疊在 Logic 運算層 (Tensor Cores) 之上。這將水平傳輸距離轉換成了極短的垂直距離。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`3d_stacked_sram_sim.py`
- **2D 平面 SRAM**: 存取延遲 45.0 ns，每位元功耗 0.8 pJ
- **3D 堆疊 SRAM**: 存取延遲 5.0 ns，每位元功耗 0.15 pJ
- **延遲加速 (Speedup)**: **9.00x**
- **功耗降低 (Power Reduction)**: **5.33x**

## 4. 硬體架構建議
針對次世代 Edge NPU，當面臨長文本 (Long-Context) 推論時，2D SRAM 已無法擴展。我們建議全面採用 SRAM-on-Logic 的 3D 封裝架構，打破面積與連線延遲的物理限制，以極低功耗容納數 GB 的 KV Cache。
