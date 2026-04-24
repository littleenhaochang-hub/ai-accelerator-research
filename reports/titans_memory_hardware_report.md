# Titans Neural Memory 硬體加速架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
最新的 Titans 架構 (Learning to Memorize at Test Time) 引入了神經記憶體 (Neural Memory)，透過在推論階段 (Test-time) 進行局部梯度下降來記住長文本上下文。然而，傳統 NPU 僅為前向傳播 (Forward Pass) 設計，若要在推論時進行反向傳播與權重更新，必須將 Activations 存回 DRAM，並排隊使用 Tensor Core 執行外積 (Outer Product) 運算，造成極大的延遲，抵銷了 Titans 架構的效率優勢。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
為了解決 Test-time Training (TTT) 的記憶體更新瓶頸，我們設計了 **In-SRAM Gradient Aggregator (SRAM 內梯度聚合器)**。該架構修改了傳統 SRAM 的 Bitline 邏輯，允許在讀取/寫入週期內，直接於記憶體陣列內部完成 $O(N)$ 的梯度外積與權重相加，完全不需要將資料搬移至主計算陣列 (MACs)。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`titans_memory_hardware_sim.py`
- **傳統數位 Backprop (MAC 陣列)**: 處理 32K Token 的記憶體更新延遲約 1474.56 us
- **SRAM 內梯度聚合器**: 延遲僅 163.84 us
- **運算加速 (Speedup)**: **9.00x**

## 4. 硬體架構建議
針對未來具備自我學習或長文本記憶能力 (如 Titans 或 TTT) 的 Edge Agent 晶片，建議將神經記憶體狀態直接實作於具備「In-SRAM Update」能力的特製快取中，讓推理與記憶體更新得以完美重疊。
