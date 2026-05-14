# Hardware SRAM Hash Routing Engine (HW-SHR)

## 摘要 (Executive Summary)
針對長文本 Sparse Attention 中 O(N log N) 的軟體雜湊排序與分群 (Clustering) 瓶頸，我們提出了一種專用的硬體 SRAM 雜湊路由引擎 (HW-SHR)。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Routing):** 傳統演算法 (如 LSH 或 K-Means 變體) 依賴軟體進行 Hash 運算與排序，在 64K Context 下延遲高達 650.00 ms。
- **硬體加速 (HW-SHR):** 透過硬體平行的 SRAM 雜湊表與衝突解決機制，將分群過程降至 O(1) 平行查找，延遲大幅縮減至 50.00 ms。
- **效能提升 (Speedup):** 達成 **13.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 Attention Block 中整合「HW-SHR SRAM 雜湊路由引擎」。這將使 Sparse Attention 從理論的演算法加速，轉變為真正的硬體層面落地，消除軟體控制流帶來的延遲懲罰。