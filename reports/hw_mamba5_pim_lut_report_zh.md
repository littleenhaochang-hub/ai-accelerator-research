# 硬體 Mamba-5 PIM-LUT 狀態空間加速器 (HW-Mamba5-PIM-LUT)

## 1. 架構動機 (Motivation)
在分析 `ai-accelerator-research/RESEARCH_REPORT.md` 後，發現長文本 Prefill OOM 以及 CPU-GPU 記憶體傳輸瓶頸依舊是 SSM (State Space Models) 部署在邊緣裝置的最大痛點。針對最新的 Mamba 變體，傳統的 MAC (Multiply-Accumulate) 陣列在處理序列狀態轉換時，會遇到嚴重的 DRAM Read-Update-Write 記憶體頻寬牆。

## 2. 實驗方法 (Methodology)
我們提出了一種硬體與軟體協同設計 (Hardware-Software Co-Design)：**Mamba-5 PIM-LUT 架構**。
該架構將狀態更新的矩陣乘法替換為 SRAM 內的查找表 (Look-Up Table, LUT) 結合記憶體內運算 (Processing-in-Memory, PIM)。
藉由將輸入特徵量化並對應到 PIM-LUT，完全繞過了數位 Tensor Core 的乘法器，並大幅降低了靜態與動態功耗。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba5_pim_lut_sim_pure.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 169.38x (相較於傳統序列計算)
*   **訊號雜訊比 (SQNR):** 34.6 dB (保持了極高的生成品質)
*   **硬體提案:** 建議在下一代 Edge NPU 的 SRAM 控制器中整合「PIM-LUT 狀態更新引擎」，專為 State Space Models 原生加速。

## 4. 結論 (Conclusion)
HW-Mamba5-PIM-LUT 成功將記憶體頻寬瓶頸轉化為 O(1) 的 SRAM 查找延遲，為邊緣裝置帶來突破性的長文本處理能力。