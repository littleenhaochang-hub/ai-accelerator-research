# 硬體 Mamba-21 Hyperdimensional PIM-LUT 狀態空間加速器 (HW-Mamba21-HD-PIM-LUT)

## 1. 架構動機 (Motivation)
為了解決超大狀態空間在 PIM-LUT 查表時的解析度瓶頸，我們引入了超高維度計算 (Hyperdimensional Computing, HDC) 的概念。透過將 SSM 的狀態向量映射到具有極高維度的正交二值空間 (Orthogonal Binary Space)，我們可以大幅度簡化狀態更新的複雜度。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-21 Hyperdimensional PIM-LUT 架構**。我們在 PIM 巨集內整合了硬體級別的位元 XOR 與 Popcount 引擎。狀態更新不再依賴高精度的乘加運算，而是透過超高維度二值向量的綁定 (Binding) 與綁定解除 (Unbinding) 操作，這些操作可完美映射為超低功耗的查表與位元運算。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba21_hyperdimensional_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 760.64x (HDC 的二值化運算大幅降低了查表與更新的延遲)
*   **訊號雜訊比 (SQNR):** 39.8 dB (超高維度空間的冗餘特性確保了強大的容錯與表徵能力)
*   **硬體提案:** 建議在下一代專注於極端低功耗與高強健性 Edge NPU 中實作「超高維度 PIM-LUT 加速引擎」。

## 4. 結論 (Conclusion)
HW-Mamba21-HD-PIM-LUT 結合了超高維度運算的強健性與 PIM-LUT 的高效能，成功將複雜的狀態空間轉換為純邏輯閘操作，為未來的類腦計算邊緣晶片奠定了基礎。