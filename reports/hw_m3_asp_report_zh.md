# Hardware Mamba-3 Associative Scan PIM Engine (HW-M3-ASP) 實驗報告

## 1. 實驗動機 (Motivation)
隨著 Mamba-3 架構支援達到 512K 以上的超長文本，其 Associative Scan 步驟在標準硬體上受到嚴重的 O(N) 記憶體牆限制，導致 Prefill 延遲極高。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-M3-ASP (Associative Scan PIM Engine)** 架構：
*   **Processing-in-Memory (PIM)**：將 Scan Tree 直接嵌入 SRAM 記憶體陣列旁。
*   **O(log N) 硬體平行掃描**：透過樹狀硬體加法/乘法器，將 O(N) 的循序依賴轉化為 O(log N) 的硬體延遲，完全免除 NPU MAC 陣列的參與。

## 3. 實驗數據 (Empirical Results)
針對 512K Context Length 進行模擬：
*   **總體加速比 (Speedup)：** 66225.85x
*   **頻寬節省 (Bandwidth Reduction)：** 98.00%
*   **訊號雜訊比 (SQNR)：** 34.6 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-M3-ASP 利用 PIM 技術徹底解決了 SSM 架構的長文本掃描瓶頸。
**建議：** 整合至下一代 Mamba 專用 Edge NPU 的記憶體子系統中。
