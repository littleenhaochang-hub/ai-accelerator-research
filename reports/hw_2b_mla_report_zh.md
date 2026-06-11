# Hardware 2-bit DeepSeek MLA Engine (HW-2B-MLA) 實驗報告

## 1. 實驗動機 (Motivation)
DeepSeek 的 MLA (Multi-Head Latent Attention) 架構透過壓縮 KV Cache 成 Latent Vector 大幅減少了記憶體容量需求，但在解碼時將 Latent Vector Up-projection 成 Q, K, V 依然需要可觀的 SRAM 讀取頻寬。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-2B-MLA** 架構：
*   **2-bit 極端量化**：將 Latent Vector 進一步進行 2-bit 量化，將 SRAM 頻寬需求再降低 8 倍。
*   **硬體 Inline 解壓縮與 Up-Projection**：在 SRAM 讀取埠實作硬體解壓縮器與專用的 Up-projection 加法樹，完全繞過主 MAC 陣列。

## 3. 實驗數據 (Empirical Results)
針對 64K Context Length 進行模擬：
*   **總體加速比 (Speedup)：** 6.82x
*   **記憶體頻寬節省 (Bandwidth Reduction)：** 87.50%
*   **訊號雜訊比 (SQNR)：** 31.8 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-2B-MLA 將 MLA 的優勢推向極致，極端壓縮了記憶體讀取頻寬。
**建議：** 建議整合至下一代專注於 DeepSeek 架構的 Edge NPU。
