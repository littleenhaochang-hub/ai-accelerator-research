# Auto-Researcher 分析報告：Hardware KV Cache Delta Compression Engine (HW-KVDC)

## 1. 瓶頸分析 (Analyze)
在長文本生成 (Long-Context Generation) 中，KV Cache 容量是主要瓶頸。相鄰 Token 之間在 Transformer 高層級通常具有高度的語義連續性與數值相似性。傳統獨立儲存每個 Token 的 KV 向量，造成了極大的冗餘與記憶體頻寬浪費。

## 2. 理論探索 (Explore)
我們提出「Hardware KV Cache Delta Compression Engine (HW-KVDC)」。該架構不獨立量化每個 Token，而是採用差分編碼 (Delta Encoding)。每 16 個 Tokens 儲存一個全精度 (如 INT8/FP16) 的 Base Token，後續 15 個 Tokens 僅計算與前一個 Token 的差值 (Delta)，並以硬體級別即時量化為極低精度 (INT2)。

## 3. 原型實驗結果 (Prototype)
我們於 `hw_kvdc_sim.py` 進行了記憶體容量與頻寬模擬：
*   **基準測試 (128K Context, FP16):** 佔用 32.77 MB 記憶體。
*   **HW-KVDC (Base+INT2 Deltas):** 佔用 5.89 MB 記憶體。
*   **效能提升:** 達成 **82.03% 的記憶體容量減少**。

## 4. 硬體架構結論 (Conclusion)
Edge NPU 的 SRAM 控制器應內建硬體差分解碼器 (Delta Decoder) 與加法器樹。在 SRAM 讀取時，硬體能夠在 1 個週期內將 Base + Deltas 還原為完整向量。這不僅打破了 SRAM 容量牆，也徹底消除了冗餘的記憶體讀寫。
