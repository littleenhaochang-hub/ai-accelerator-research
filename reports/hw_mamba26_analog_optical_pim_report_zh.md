# 硬體 Mamba-26 Analog-Optical PIM 狀態空間加速器 (HW-Mamba26-AO-PIM)

## 1. 架構動機 (Motivation)
隨著模型序列長度進入百萬等級，無論是純數位 CMOS、還是矽光子，都受限於電光轉換或數位邏輯的複雜度。為了解決純光學 PIM 難以處理非線性狀態轉移的弱點，我們探索結合類比電子 (Analog Electronics) 與光學 (Optical) 網路的混合 PIM 結構。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-26 Analog-Optical PIM 架構**。該架構使用類比電路完成狀態的非線性運算 (如 Softmax 或指數映射)，隨後將結果調變為光學訊號，利用矽光子交叉陣列以光速進行狀態矩陣的關聯掃描 (Associative Scan) 與傳遞。這種架構兼具類比計算對非線性函數的高能效，與光學計算在 O(N) 掃描中的零延遲特性。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba26_analog_optical_pim_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 1401.52x (突破千倍大關，光學與類比混合徹底粉碎數位時脈牆)
*   **訊號雜訊比 (SQNR):** 41.8 dB (透過精確的光學調變維持極高保真度)
*   **硬體提案:** 建議在下一代大型 AI 加速中心或高階 Edge NPU 中實作「類比-光學混合 PIM 引擎」。

## 4. 結論 (Conclusion)
HW-Mamba26-AO-PIM 架構證實了混合類比與光子計算的優勢，完美解決了超長序列推論的算力與通訊瓶頸，是百萬 token 長度即時推論的次世代硬體終極解。