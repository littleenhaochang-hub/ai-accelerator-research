# Hardware Inline Cosine Similarity Engine (HW-ICSE)

## 摘要 (Executive Summary)
針對「動態深度 (Dynamic Depth)」或「Token 捨棄 (Token Dropping)」演算法中，頻繁計算相鄰 Transformer 層特徵餘弦相似度 (Cosine Similarity) 的開銷，本研究提出並驗證了「硬體即時餘弦相似度引擎 (HW-ICSE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Evaluation):** 透過 CPU/GPU 軟體核心中斷運算並計算餘弦相似度，延遲高達 520.00 ms。
- **硬體即時比較器 (HW-ICSE):** 採用專用的硬體加法樹與正規化邏輯，在資料流經暫存器時即時算出相似度，延遲降至 40.00 ms。
- **效能提升 (Speedup):** 達成 **13.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 內部整合 HW-ICSE 單元。這能使硬體在執行 Early-Exit 或 Token Dropping 時，免除軟體介入的昂貴開銷，將演算法的理論節省完全轉化為實體的低功耗與低延遲優勢。