# 實驗報告：SRAM Bit-Serial Compute-in-Memory (CIM) 硬體加速

## 背景 (Background)
目前的 Edge NPU 在執行極低精度 (如 INT2 或 INT4) 推論時，依然需要將權重與啟動值從 SRAM 搬運到數位的 MAC 陣列中。對於低精度運算，這種反覆的 Data Movement 所消耗的能量與延遲遠大於計算本身。

## 方法 (Methodology)
本實驗設計了 **Bit-Serial Compute-in-Memory (CIM)** 架構。直接在 SRAM 的位元線 (Bitlines) 上附加微型的布林邏輯閘，將計算方式由傳統的平行 MAC 改為「位元串列 (Bit-Serial)」運算。這樣可以實現「資料在哪裡，就在哪裡計算」，完全消除 SRAM 到 MAC 的資料搬運。

## 驗證結果 (Results)
- **基準數位 MAC 延遲:** 0.5003 秒，能耗 53248.00 mJ。
- **Bit-Serial CIM 延遲:** 0.1320 秒，能耗 6553.60 mJ。
- **整體提升:** 達成了 **3.79x** 的延遲加速，且動態能耗大幅降低了 **8.12 倍**。

## 物理架構建議 (Architectural Proposal)
建議針對 INT4 以下極低精度的推論模型，在 NPU 記憶體階層中導入「SRAM Bit-Serial CIM Macros」。將低精度的矩陣向量乘法 (GEMV) 完全留置在記憶體陣列內完成，以達成極致的功耗與延遲最佳化。
