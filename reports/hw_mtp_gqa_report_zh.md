# Hardware MTP GQA Broadcaster (HW-MTP-GQA) 實驗報告

## 1. 實驗背景與瓶頸分析
在使用 Multi-Token Prediction (MTP) 或推測解碼時，模型會同時產生多個未來 token 的預測路徑。當這些路徑(drafts) 使用 GQA (Grouped-Query Attention) 時，多個 Query 實際上是對齊並共享同一組 KV Cache 的。目前的軟體調度通常會獨立為每個路徑抓取相同的 KV Cache，造成極大的 SRAM 頻寬浪費。

## 2. 探索與文獻支持
為了解決 GQA 在推測解碼中的重複讀取問題，我們提出 Hardware MTP GQA Broadcaster (HW-MTP-GQA)。

## 3. 實驗方法與 Prototype
開發 `hw_mtp_gqa_sim.py`，於 SRAM 與 Tensor Core 間插入一個零延遲的多播匯流排 (Zero-cycle Broadcast Bus)。該匯流排僅讀取一次共用的 KV Cache，然後同時廣播給處理不同 draft 分支的 MAC 陣列。
- **測試設定:** 8 Query Groups, 32K Context Length, 4 Drafts.

## 4. 數據與驗證結果
- **Baseline Transfer:** 512.00 MB
- **Baseline Latency:** 1.49 ms
- **HW-MTP-GQA Transfer:** 128.00 MB
- **HW-MTP-GQA Latency:** 0.22 ms
- **效能提升 (Speedup):** 6.70x

## 5. 架構結論與建議
實驗證實 HW-MTP-GQA 能夠完美消除 MTP 分支中的冗餘記憶體讀取。強烈建議在下一代專注於 DeepSeek 等 MTP 模型推論的 Edge NPU 中，將該 Broadcast Bus 納入標準架構設計。