# Auto-Researcher 實驗報告：W4A4 與 QJL KV Cache 量化架構
**日期:** 2026-04-13

## 1. 瓶頸分析
根據目前的 `RESEARCH_REPORT.md`，邊緣設備 (如 Mac mini, Edge NPU) 在運行大規模 LLM 時面臨嚴重的「記憶體牆 (Memory Wall)」。
1. **Weight Footprint:** FP16 權重導致記憶體頻寬耗盡。
2. **KV Cache Footprint:** 長文本推理時，KV Cache 的成長速度極快，甚至超過模型權重本身，導致 Out-of-Memory (OOM)。

## 2. 文獻探索
透過檢索 2025/2026 arXiv, ICLR 2025, MLSys 2025 論文，我們發現：
*   **QJL (Quantized Johnson-Lindenstrauss):** 針對 KV Cache 壓縮的新方法。利用 JL Transform 作為 preconditioner，再量化為 1-bit，且達到「零記憶體額外開銷 (zero memory overhead)」。已被 MLSys 2025 接受。
*   **W4A4 推理 (COMET, LO-BCQ, QUAD, QRazor):** 全面推進 4-bit 權重與 4-bit Activation。利用 SVD 分解 activation outliers 或群集編碼，確保 W4A4 下的精度不流失。

## 3. Prototype 驗證
我們開發了 `w4a4_qjl_prototype.py` 根據 Roofline Model 進行了 Edge 記憶體頻寬模擬 (以 8B 模型，Batch 32, Seq 4096 為例)：
*   **FP16 基準:** 權重 16GB + KV Cache 68.7GB，總佔用 84.7GB。 TPS 僅約 3.5。
*   **W4A4 + 1-bit QJL:** 權重壓縮至 4GB + KV Cache 壓縮至 4.29GB，總佔用僅 8.29GB。
*   **理論加速與記憶體減免:** 記憶體佔用降低 10 倍，在 Memory-bound 假設下，**推論 TPS 獲得 10.21x 的提升** (3.5 -> 36.17 tokens/s)。

## 4. 結論
W4A4 搭配 1-bit QJL 是 2026 年邊緣 AI 加速器的黃金組合。在硬體架構 (Hardware Architecture) 設計上，我們必須：
1. 實作原生的 **INT4 Tensor Cores** (取代 INT8/FP16)。
2. 針對 QJL 1-bit KV Cache，設計專屬的 **Bit-wise XNOR 與 POPCNT (Population Count) 運算單元** 來執行高速 Attention Score 計算，這將能以極低功耗達成超長文本處理。此發現已整合入我們的 Auto-Research 藍圖。
