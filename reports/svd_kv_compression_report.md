# SVD 低秩 KV Cache 壓縮硬體架構分析

## 實驗背景
為了突破 Edge 裝置的記憶體容量天花板，我們探討了利用 SVD (奇異值分解) 對長文本 KV Cache 進行低秩近似壓縮 (Low-Rank Approximation) 的可行性。我們嘗試將巨大的 $N \times D$ 矩陣分解為 $N \times r$ 與 $r \times D$ 兩個小矩陣儲存。

## 實驗方法
撰寫 `svd_kv_compression_sim.py`，模擬 8K Context 下，將 4096 維度的 KV 矩陣以 Rank $r=128$ 進行壓縮。計算壓縮前後的記憶體容量、頻寬讀取時間，以及硬體重建 (Reconstruction) 所需的額外 MAC 運算延遲。

## 實驗數據
- **Baseline KV Memory**: 134.22 MB
- **SVD Low-Rank KV Memory**: 6.29 MB
- **Memory Capacity Reduction**: 95.31%
- **Effective Speedup (Fetch + Reconstruct)**: 7.00x

## 硬體架構結論
SVD 低秩壓縮能夠極致地將 KV Cache 容量**縮減高達 95.31%**，帶來了 7 倍的整體延遲改善。
然而，從壓縮矩陣重建回原始特徵需要高達數 TFLOPs 的額外運算開銷。如果佔用主 MAC 陣列，會嚴重干擾正常的 Attention 與 FFN 執行。未來的 Edge NPU 必須在記憶體匯流排旁整合專屬的 **Low-Rank Tensor Reconstructor (低秩張量重建引擎)**，使矩陣還原能與 SRAM 讀取操作完美重疊 (Pipelined)，在不消耗主算力的情況下達成極端記憶體壓縮。
